"""OpenTelemetry: mọi bước của agent ghi một span.

Dùng TracerProvider riêng của ứng dụng (không đụng provider toàn cục), nên có thể cấu hình
lại nhiều lần — kiểm thử gắn InMemorySpanExporter để khẳng định các span được tạo ra.

Tên span (xem docs/architecture.md):
  agent.session · planner.plan · llm.complete · orchestrator.iteration ·
  guarded_tool.call (thuộc tính ``decision``) · tool.execute · injection_guard.scan ·
  evidence.append · report.synthesize · rag.verify
"""

from __future__ import annotations

import threading
from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from typing import Any

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
    SimpleSpanProcessor,
)
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from opentelemetry.trace import Status, StatusCode

from app.errors import (
    AgentError,
    BudgetExceededError,
    InvalidToolArgumentsError,
    ToolNotAllowedError,
)

# Kết quả "bình thường" của luồng điều khiển: không đánh dấu span là ERROR.
_EXPECTED = (ToolNotAllowedError, BudgetExceededError, InvalidToolArgumentsError)

_lock = threading.Lock()
_provider: TracerProvider | None = None
_tracer: trace.Tracer | None = None


def configure_telemetry(
    kind: str = "none",
    *,
    service_name: str = "aik08-agent",
    in_memory: bool = False,
) -> InMemorySpanExporter | None:
    """Thiết lập (hoặc thiết lập lại) nơi xuất span. Trả về exporter bộ nhớ nếu ``in_memory``."""
    global _provider, _tracer
    provider = TracerProvider(resource=Resource.create({"service.name": service_name}))
    memory: InMemorySpanExporter | None = None

    if in_memory:
        memory = InMemorySpanExporter()
        provider.add_span_processor(SimpleSpanProcessor(memory))
    elif kind == "console":
        provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
    elif kind == "otlp":
        # Địa chỉ lấy từ OTEL_EXPORTER_OTLP_ENDPOINT (mặc định http://localhost:4318).
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

        provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
    elif kind not in ("none", ""):
        raise ValueError(f"OTEL_EXPORTER không hợp lệ: {kind!r} (none | console | otlp)")

    with _lock:
        old = _provider
        _provider = provider
        _tracer = provider.get_tracer("aik08")
    if old is not None:
        old.shutdown()
    return memory


def shutdown_telemetry() -> None:
    global _provider, _tracer
    with _lock:
        provider, _provider, _tracer = _provider, None, None
    if provider is not None:
        provider.shutdown()


def get_tracer() -> trace.Tracer:
    global _tracer
    if _tracer is None:
        configure_telemetry("none")
    assert _tracer is not None
    return _tracer


def _clean(attributes: Mapping[str, Any] | None) -> dict[str, Any]:
    """OpenTelemetry chỉ nhận str/bool/int/float (và dãy của chúng)."""
    out: dict[str, Any] = {}
    for key, value in (attributes or {}).items():
        if value is None:
            continue
        out[key] = value if isinstance(value, (str, bool, int, float)) else str(value)
    return out


@contextmanager
def span(name: str, attributes: Mapping[str, Any] | None = None) -> Iterator[trace.Span]:
    """Mở một span con của span hiện tại.

    * Lỗi miền "dự kiến" (bị chặn, hết ngân sách, tham số sai): ghi sự kiện, KHÔNG đánh dấu ERROR.
    * Lỗi khác: ghi exception và đặt trạng thái ERROR.
    """
    with get_tracer().start_as_current_span(
        name,
        attributes=_clean(attributes),
        record_exception=False,
        set_status_on_exception=False,
    ) as current:
        try:
            yield current
        except _EXPECTED as exc:
            current.set_attribute("outcome", getattr(exc, "code", "expected"))
            current.add_event("agent.expected_stop", {"error.code": getattr(exc, "code", ""), "message": str(exc)})
            raise
        except AgentError as exc:
            current.set_attribute("error.code", exc.code)
            current.record_exception(exc)
            current.set_status(Status(StatusCode.ERROR, str(exc)))
            raise
        except BaseException as exc:
            current.record_exception(exc)
            current.set_status(Status(StatusCode.ERROR, str(exc)))
            raise


def set_attributes(current: trace.Span, attributes: Mapping[str, Any]) -> None:
    for key, value in _clean(attributes).items():
        current.set_attribute(key, value)
