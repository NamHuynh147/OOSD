"""Bọc một LLMProvider để mỗi lời gọi tạo một span ``llm.complete`` (purpose, nhà cung cấp, token, thời lượng)."""

from __future__ import annotations

from app.llm.provider import LLMProvider, LLMResponse, timeout_kwargs
from app.telemetry.otel import set_attributes, span


class TracedLLM:
    def __init__(self, inner: LLMProvider) -> None:
        self.inner = inner

    @property
    def name(self) -> str:
        return str(getattr(self.inner, "name", "unknown"))

    @property
    def model(self) -> str:
        return str(getattr(self.inner, "model", "unknown"))

    def complete(self, *, system: str, user: str, purpose: str, timeout_seconds: float | None = None) -> LLMResponse:
        with span(
            "llm.complete",
            {
                "llm.purpose": purpose,
                "llm.provider": self.name,
                "llm.model": self.model,
                "llm.timeout_seconds": timeout_seconds,
            },
        ) as current:
            response = self.inner.complete(
                system=system, user=user, purpose=purpose, **timeout_kwargs(self.inner, timeout_seconds)
            )
            set_attributes(
                current,
                {
                    "llm.input_tokens": response.input_tokens,
                    "llm.output_tokens": response.output_tokens,
                    "llm.duration_ms": response.duration_ms,
                },
            )
            return response
