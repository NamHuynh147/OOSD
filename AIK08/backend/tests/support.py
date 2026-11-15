"""Công cụ dùng chung cho test: LLM giả lập có kịch bản, móc chặn thời điểm, công cụ chậm."""

from __future__ import annotations

import json
import threading
import time
from collections.abc import Sequence
from typing import Any

from app.core.text import estimate_tokens
from app.errors import LLMError
from app.llm.provider import LLMResponse, MockLLMProvider

PLAN = json.dumps(
    {
        "steps": [
            {"title": "Xác định phạm vi", "goal": "g", "tool_hint": "search_documents"},
            {"title": "Tra cứu", "goal": "g", "tool_hint": "search_documents"},
            {"title": "Đối chiếu", "goal": "g", "tool_hint": "read_document"},
        ]
    },
    ensure_ascii=False,
)
FINISH = json.dumps({"kind": "finish", "rationale": "đủ bằng chứng"})
DEFAULT_SYNTH = "## Báo cáo\n\nQuy định sao lưu thanh toán [E1]."


def act(tool: str, **arguments: Any) -> str:
    return json.dumps({"kind": "tool", "tool": tool, "arguments": arguments, "rationale": "r"}, ensure_ascii=False)


class ScriptedLLM:
    """LLM có kịch bản. ``acts``: danh sách quyết định lần lượt (lặp phần tử cuối khi hết); phần tử là
    chuỗi hoặc một ngoại lệ sẽ được ném. ``delays``: giây chờ theo purpose; nếu lớn hơn ``timeout_seconds``
    truyền vào thì ném LLMError như một provider thật bị hết thời gian."""

    name, model = "scripted", "s-1"

    def __init__(
        self,
        acts: Sequence[Any] = (),
        *,
        synth: str = DEFAULT_SYNTH,
        plan: str = PLAN,
        delays: dict[str, float] | None = None,
        hooks: dict[tuple[str, int], tuple[threading.Event, float]] | None = None,
    ):
        self.acts, self.synth, self.plan = list(acts), synth, plan
        self.delays, self.hooks = delays or {}, hooks or {}
        self.counts: dict[str, int] = {}
        self.calls: list[tuple[str, float]] = []
        self.prompts: list[tuple[str, str]] = []
        self._t0 = time.monotonic()

    def complete(self, *, system: str, user: str, purpose: str, timeout_seconds: float | None = None) -> LLMResponse:
        self.counts[purpose] = self.counts.get(purpose, 0) + 1
        self.calls.append((purpose, round(time.monotonic() - self._t0, 2)))
        self.prompts.append((purpose, user))
        hook = self.hooks.get((purpose, self.counts[purpose]))
        if hook:
            hook[0].set()
            time.sleep(hook[1])
        delay = self.delays.get(purpose, 0.0)
        if delay:
            if timeout_seconds is not None and delay > timeout_seconds:
                time.sleep(timeout_seconds)
                raise LLMError("hết thời gian chờ LLM (giả lập)")
            time.sleep(delay)
        if purpose == "plan":
            text = self.plan
        elif purpose == "act":
            index = min(self.counts["act"] - 1, len(self.acts) - 1) if self.acts else -1
            item = self.acts[index] if index >= 0 else FINISH
            if isinstance(item, BaseException):
                raise item
            text = item
        elif purpose == "synthesize":
            text = self.synth
        elif purpose == "verify":
            labels = [int(p["label"][1:]) for p in json.loads(user)["retrieved_evidence"]]
            text = json.dumps({"verdict": "supported", "issues": [], "checked_citations": labels})
        else:
            text = "{}"
        return LLMResponse(text, self.name, self.model, estimate_tokens(system + user), estimate_tokens(text), 1)


class HookedMock:
    """MockLLMProvider có thể giữ một lời gọi (lần thứ ``nth`` của ``purpose``) trong ``hold`` giây."""

    name, model = "mock", "mock-v1"

    def __init__(self, purpose: str | None = None, nth: int = 1, hold: float = 1.0, synth_delay: float = 0.0):
        self.inner = MockLLMProvider()
        self.purpose, self.nth, self.hold, self.synth_delay = purpose, nth, hold, synth_delay
        self.entered = threading.Event()
        self.counts: dict[str, int] = {}
        self.calls: list[str] = []

    def complete(self, *, system: str, user: str, purpose: str, timeout_seconds: float | None = None) -> LLMResponse:
        self.counts[purpose] = self.counts.get(purpose, 0) + 1
        self.calls.append(purpose)
        if purpose == self.purpose and self.counts[purpose] == self.nth:
            self.entered.set()
            time.sleep(self.hold)
        if purpose in ("synthesize", "verify") and self.synth_delay:
            time.sleep(self.synth_delay)
        return self.inner.complete(system=system, user=user, purpose=purpose)


class SlowTool:
    """Bọc một công cụ thật: báo hiệu khi bắt đầu chạy rồi giữ nó ``hold`` giây."""

    def __init__(self, inner: Any, entered: threading.Event, hold: float):
        self.inner, self.entered, self.hold = inner, entered, hold
        self.name, self.description = inner.name, inner.description

    def validate(self, arguments: dict[str, Any]) -> object:
        return self.inner.validate(arguments)

    def execute(self, arguments: dict[str, Any]) -> Any:
        self.entered.set()
        time.sleep(self.hold)
        return self.inner.execute(arguments)
