"""LLM provider adapters and role-based routing for the read-only agent."""

from __future__ import annotations

import inspect
import json
import re
import time
from dataclasses import dataclass
from typing import Protocol

import httpx

from app.core.text import estimate_tokens
from app.errors import LLMError


@dataclass(frozen=True, slots=True)
class LLMResponse:
    text: str
    provider: str
    model: str
    input_tokens: int
    output_tokens: int
    duration_ms: int


def effective_timeout(default: float, limit: float | None) -> float:
    """Timeout thực dùng: không vượt thời gian còn lại của phiên (``limit``), tối thiểu 0,5 giây."""
    return default if limit is None else max(0.5, min(default, limit))


def timeout_kwargs(llm: object, timeout_seconds: float | None) -> dict[str, float]:
    """Chỉ truyền ``timeout_seconds`` cho provider có tham số này (provider tự viết trong test có thể không có)."""
    if timeout_seconds is None:
        return {}
    try:
        params = inspect.signature(llm.complete).parameters  # type: ignore[attr-defined]
    except (TypeError, ValueError, AttributeError):
        return {}
    return {"timeout_seconds": timeout_seconds} if "timeout_seconds" in params else {}


class LLMProvider(Protocol):
    name: str
    model: str

    def complete(
        self,
        *,
        system: str,
        user: str,
        purpose: str,
        timeout_seconds: float | None = None,
    ) -> LLMResponse: ...


class MockLLMProvider:
    """Nhà cung cấp offline, xác định, KHÔNG suy luận ngữ nghĩa.

    * ``act``: chạy kịch bản demo — tìm kiếm, rồi đọc tài liệu đầu tiên tìm được, rồi (nếu công cụ HTTP được
      cấp và có ``api_base_url``) gọi API demo, rồi kết thúc.
    * ``synthesize``: chỉ TRÍCH NGUYÊN VĂN từ bằng chứng, mỗi dòng dạng ``«trích đoạn» [E#]``.
    * ``verify``: kiểm tra bằng đối chiếu chuỗi: mỗi trích đoạn phải nằm nguyên văn trong bằng chứng nó trích.
    Nhờ vậy luồng đầy đủ (tổng hợp có trích dẫn + kiểm chứng) chạy được offline mà không giả vờ hiểu nghĩa.
    """

    name = "mock"
    model = "mock-v1"
    QUOTE_CHARS = 280

    def __init__(self, api_base_url: str = "", delay_seconds: float = 0.0) -> None:
        self.api_base_url = api_base_url.rstrip("/")
        self.delay_seconds = max(0.0, delay_seconds)

    def complete(
        self,
        *,
        system: str,
        user: str,
        purpose: str,
        timeout_seconds: float | None = None,
    ) -> LLMResponse:
        started = time.monotonic()
        if self.delay_seconds:
            time.sleep(
                min(self.delay_seconds, timeout_seconds)
                if timeout_seconds
                else self.delay_seconds
            )
        if purpose == "plan":
            text = (
                '{"steps":[{"title":"Xác định phạm vi câu hỏi","goal":"Làm rõ các khía cạnh cần tra cứu","tool_hint":"search_documents"},'
                '{"title":"Tra cứu tài liệu liên quan","goal":"Tìm nguồn nội bộ có liên quan","tool_hint":"search_documents"},'
                '{"title":"Đối chiếu bằng chứng","goal":"Đọc tài liệu gốc để kiểm chứng thông tin","tool_hint":"read_document"}]}'
            )
        elif purpose == "act":
            text = self._act(user)
        elif purpose == "synthesize":
            text = self._synthesize(user)
        elif purpose == "verify":
            text = self._verify(user)
        else:
            text = "{}"
        return LLMResponse(
            text,
            self.name,
            self.model,
            estimate_tokens(system + user),
            estimate_tokens(text),
            int((time.monotonic() - started) * 1000),
        )

    # ------------------------------------------------------------------ act
    def _act(self, user: str) -> str:
        try:
            payload = json.loads(user)
        except ValueError:
            payload = {}
        names = {
            t.get("name")
            for t in payload.get("allowed_tools", [])
            if isinstance(t, dict)
        }
        prior = [
            r for r in payload.get("prior_tool_results", []) if isinstance(r, dict)
        ]
        attempted = {r.get("tool") for r in prior}
        query = str(payload.get("query", "tra cứu tài liệu liên quan"))
        if "search_documents" in names and "search_documents" not in attempted:
            action = {
                "kind": "tool",
                "tool": "search_documents",
                "arguments": {"query": query[:300], "top_k": 5},
                "rationale": "Tra cứu nguồn nội bộ liên quan đến yêu cầu.",
            }
        elif (
            "read_document" in names
            and "read_document" not in attempted
            and (doc_id := _first_doc_id(prior))
        ):
            action = {
                "kind": "tool",
                "tool": "read_document",
                "arguments": {"doc_id": doc_id},
                "rationale": "Đọc toàn văn tài liệu liên quan nhất để đối chiếu.",
            }
        elif (
            "http_get_api" in names
            and "http_get_api" not in attempted
            and self.api_base_url
        ):
            action = {
                "kind": "tool",
                "tool": "http_get_api",
                "arguments": {"url": f"{self.api_base_url}/demo/status"},
                "rationale": "Đối chiếu với trạng thái dịch vụ hiện tại từ API demo.",
            }
        else:
            action = {
                "kind": "finish",
                "rationale": "Kịch bản demo mock đã chạy xong các công cụ.",
            }
        return json.dumps(action, ensure_ascii=False)

    # ----------------------------------------------------------- synthesize
    def _synthesize(self, user: str) -> str:
        evidence = _evidence_from_prompt(user)
        lines = [
            "## Báo cáo (chế độ mock)",
            "",
            "Bản tổng hợp tự động, chỉ trích nguyên văn từ bằng chứng; không suy luận hay diễn giải thêm.",
            "",
            "### Các điểm chính",
        ]
        for item in evidence:
            if item.get("flagged"):
                continue
            quote = (
                " ".join(str(item.get("content", "")).split())[: self.QUOTE_CHARS]
                .replace("«", "")
                .replace("»", "")
            )
            if quote:
                lines.append(
                    f"- **{item.get('title', '')}**: «{quote}» [{item.get('label', 'E?')}]"
                )
        lines += [
            "",
            "### Hạn chế",
            "- Đây là đầu ra của nhà cung cấp mock; hãy đối chiếu các bằng chứng được trích dẫn.",
        ]
        return "\n".join(lines)

    # --------------------------------------------------------------- verify
    @staticmethod
    def _verify(user: str) -> str:
        try:
            payload = json.loads(user)
            passages = {
                int(p["label"][1:]): " ".join(str(p["content"]).split())
                for p in payload["retrieved_evidence"]
            }
            must = [int(n) for n in payload.get("must_check_citations", [])]
            report = str(payload["draft_report_to_check"])
        except (ValueError, KeyError, TypeError):
            return '{"verdict":"insufficient","issues":["payload không đọc được"],"checked_citations":[]}'
        issues: list[str] = []
        for line in report.splitlines():
            labels = [int(n) for n in re.findall(r"\[E(\d{1,6})\]", line)]
            quotes = re.findall(r"«([^»]+)»", line)
            if not labels:
                continue
            if not quotes:
                issues.append(
                    f"dòng có trích dẫn nhưng không có trích đoạn nguyên văn: {line[:60]}"
                )
            for quote in quotes:
                if not any(quote in passages.get(n, "") for n in labels):
                    issues.append(
                        f"trích đoạn không có trong bằng chứng {labels}: {quote[:60]}"
                    )
        verdict = "supported" if not issues and must else "unsupported"
        return json.dumps(
            {"verdict": verdict, "issues": issues[:5], "checked_citations": must},
            ensure_ascii=False,
        )


def _first_doc_id(prior: list[dict]) -> str | None:
    for result in prior:
        for item in result.get("items", []) or []:
            if isinstance(item, dict) and item.get("doc_id"):
                return str(item["doc_id"])
    return None


def _evidence_from_prompt(user: str) -> list[dict]:
    marker = "Bằng chứng JSON (dữ liệu không đáng tin):\n"
    start = user.find(marker)
    if start < 0:
        return []
    try:
        data = json.loads(user[start + len(marker) :])
    except ValueError:
        return []
    return [d for d in data if isinstance(d, dict)] if isinstance(data, list) else []


class OpenAICompatibleProvider:
    """Adapter for the OpenAI Chat Completions API."""

    name = "openai-compatible"

    def __init__(
        self, *, api_key: str, model: str, base_url: str, timeout_seconds: float = 30.0
    ) -> None:
        if not api_key.strip():
            raise ValueError("Thiếu OPENAI_API_KEY cho OpenAI-compatible provider")
        self.api_key = api_key.strip()
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds

    def complete(
        self,
        *,
        system: str,
        user: str,
        purpose: str,
        timeout_seconds: float | None = None,
    ) -> LLMResponse:
        started = time.monotonic()
        models_to_try = [self.model]
        if self.model != "qwen/qwen3.8-27b" and "groq.com" in self.base_url:
            models_to_try.append("qwen/qwen3.8-27b")

        last_error: LLMError | None = None
        for current_model in models_to_try:
            body: dict[str, object] = {
                "model": current_model,
                "temperature": 0,
                "max_tokens": {
                    "plan": 1024,
                    "act": 1024,
                    "synthesize": 2500,
                    "verify": 1024,
                }.get(purpose, 1024),
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
            }
            if purpose in {"plan", "act", "verify"}:
                body["response_format"] = {"type": "json_object"}
            if "gpt-oss" in current_model:
                body["reasoning_effort"] = "low"

            try:
                with httpx.Client(
                    timeout=effective_timeout(self.timeout_seconds, timeout_seconds),
                    follow_redirects=False,
                ) as client:
                    response = client.post(
                        f"{self.base_url}/chat/completions",
                        headers={
                            "Authorization": f"Bearer {self.api_key}",
                            "Content-Type": "application/json",
                            "User-Agent": "AIK08-Client/1.0",
                        },
                        json=body,
                    )
                    if response.status_code == 429:
                        last_error = LLMError(
                            f"Groq 429 TPM limit trên model {current_model}"
                        )
                        continue
                    response.raise_for_status()
                    payload = response.json()
                text = payload["choices"][0]["message"]["content"]
                text = re.sub(
                    r"<think>.*?</think>\s*", "", text, flags=re.DOTALL
                ).strip()
                if not text:
                    raise ValueError("LLM trả về nội dung rỗng")
                usage = payload.get("usage") or {}
                return LLMResponse(
                    text,
                    self.name,
                    current_model,
                    int(usage.get("prompt_tokens", estimate_tokens(system + user))),
                    int(usage.get("completion_tokens", estimate_tokens(text))),
                    int((time.monotonic() - started) * 1000),
                )
            except httpx.HTTPStatusError as exc:
                detail = exc.response.text.strip().replace("\n", " ")[:200]
                last_error = LLMError(
                    f"OpenAI endpoint lỗi HTTP {exc.response.status_code}: {detail}"
                )
            except (
                httpx.HTTPError,
                ValueError,
                KeyError,
                IndexError,
                TypeError,
            ) as exc:
                last_error = LLMError(
                    f"Gọi OpenAI-compatible endpoint thất bại ({type(exc).__name__}: {exc})"
                )
        assert last_error is not None
        raise last_error


class GeminiProvider:
    """Adapter for Google's Gemini generateContent REST API."""

    name = "google"

    def __init__(
        self, *, api_key: str, model: str, base_url: str, timeout_seconds: float = 30.0
    ) -> None:
        keys = [k.strip() for k in api_key.split(",") if k.strip()]
        if not keys:
            raise ValueError("Thiếu GEMINI_API_KEY cho Google Gemini provider")
        self.api_keys = keys
        self.api_key = keys[0]
        self.model = model.strip()
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds

    def complete(
        self,
        *,
        system: str,
        user: str,
        purpose: str,
        timeout_seconds: float | None = None,
    ) -> LLMResponse:
        started = time.monotonic()
        url = f"{self.base_url}/v1beta/models/{self.model}:generateContent"
        payload = {
            "systemInstruction": {"parts": [{"text": system}]},
            "contents": [{"role": "user", "parts": [{"text": user}]}],
            "generationConfig": {
                "temperature": 0,
                "maxOutputTokens": {"plan": 4096, "act": 4096, "synthesize": 8192}.get(
                    purpose, 4096
                ),
                "responseMimeType": (
                    "application/json"
                    if purpose in {"plan", "act", "verify"}
                    else "text/plain"
                ),
            },
        }
        last_error: LLMError | None = None
        for key in self.api_keys:
            try:
                with httpx.Client(
                    timeout=effective_timeout(self.timeout_seconds, timeout_seconds),
                    follow_redirects=False,
                ) as client:
                    response = client.post(
                        url, headers={"x-goog-api-key": key}, json=payload
                    )
                    response.raise_for_status()
                    result = response.json()
                candidates = result.get("candidates") or []
                if not candidates:
                    raise ValueError(
                        f"Gemini không trả về candidates (promptFeedback={result.get('promptFeedback')})"
                    )
                parts = (candidates[0].get("content") or {}).get("parts") or []
                # Bỏ qua các phần suy luận nội bộ (thought=True) để không làm hỏng JSON đầu ra
                text = "".join(
                    part.get("text", "")
                    for part in parts
                    if isinstance(part, dict) and not part.get("thought")
                )
                if not text.strip():
                    finish = candidates[0].get("finishReason")
                    raise ValueError(
                        f"Gemini trả về nội dung rỗng (finishReason={finish})"
                    )
                usage = result.get("usageMetadata") or {}
                return LLMResponse(
                    text,
                    self.name,
                    self.model,
                    int(usage.get("promptTokenCount", estimate_tokens(system + user))),
                    int(usage.get("candidatesTokenCount", estimate_tokens(text))),
                    int((time.monotonic() - started) * 1000),
                )
            except httpx.HTTPStatusError as exc:
                detail = exc.response.text.strip().replace("\n", " ")[:220]
                last_error = LLMError(
                    f"Gemini lỗi HTTP {exc.response.status_code}: {detail}"
                )
            except (
                httpx.HTTPError,
                ValueError,
                KeyError,
                IndexError,
                TypeError,
            ) as exc:
                last_error = LLMError(
                    f"Gọi Gemini thất bại ({type(exc).__name__}: {exc})"
                )
        assert last_error is not None
        raise last_error


class RoleBasedLLMProvider:
    """Routes planning/agent decisions to Gemini and report synthesis to an OpenAI-compatible endpoint."""

    name = "multi-role"

    def __init__(self, *, primary: LLMProvider, synthesizer: LLMProvider) -> None:
        self.primary = primary
        self.synthesizer = synthesizer
        self.model = f"plan-act:{primary.model};synthesize:{synthesizer.model}"

    def complete(
        self,
        *,
        system: str,
        user: str,
        purpose: str,
        timeout_seconds: float | None = None,
    ) -> LLMResponse:
        # Tool selection is always performed by the primary Gemini model. The secondary
        # OpenAI-compatible endpoint only drafts a report from guarded-tool evidence.
        provider = self.synthesizer if purpose == "synthesize" else self.primary
        return provider.complete(
            system=system, user=user, purpose=purpose, timeout_seconds=timeout_seconds
        )


def build_provider(settings: object) -> LLMProvider:
    provider = str(getattr(settings, "llm_provider", "mock")).strip().lower()
    timeout = getattr(settings, "llm_timeout_seconds", 30.0)
    if provider == "mock":
        return MockLLMProvider(
            api_base_url=str(getattr(settings, "public_base_url", "")),
            delay_seconds=float(getattr(settings, "mock_llm_delay_seconds", 0.0)),
        )
    if provider == "openai":
        return OpenAICompatibleProvider(
            api_key=settings.openai_api_key,
            model=settings.openai_model,
            base_url=settings.openai_base_url,
            timeout_seconds=timeout,
        )
    if provider == "google":
        return GeminiProvider(
            api_key=settings.gemini_api_key,
            model=settings.gemini_model,
            base_url=settings.gemini_base_url,
            timeout_seconds=timeout,
        )
    if provider == "multi":
        primary = GeminiProvider(
            api_key=settings.gemini_api_key,
            model=settings.gemini_model,
            base_url=settings.gemini_base_url,
            timeout_seconds=timeout,
        )
        secondary = OpenAICompatibleProvider(
            api_key=settings.openai_api_key,
            model=settings.openai_model,
            base_url=settings.openai_base_url,
            timeout_seconds=timeout,
        )
        return RoleBasedLLMProvider(primary=primary, synthesizer=secondary)
    raise ValueError(
        f"LLM_PROVIDER không được hỗ trợ: {provider!r}; dùng mock, google, openai hoặc multi"
    )
