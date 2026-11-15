"""T3/T4 — hủy phiên ở mọi thời điểm vẫn trả về phần báo cáo đã có (PostgreSQL thật)."""

from __future__ import annotations

import threading
import time
from typing import Any

import pytest

from app.core.models import Limits, ReportStatus, SessionStatus, StopReason
from tests.support import HookedMock, SlowTool

pytestmark = pytest.mark.postgres
QUERY = "quy trình ứng phó sự cố và SLA"


def run_with_cancel(
    sessions: Any,
    orch: Any,
    llm: Any,
    *,
    when: str,
    entered: threading.Event | None = None,
    limits: Limits = Limits(10, 20000, 60),
) -> tuple[Any, Any, dict[str, Any]]:
    session = sessions.create(QUERY, limits)
    out: dict[str, Any] = {}

    def runner() -> None:
        try:
            out["report"] = orch.run(session.id)
        except Exception as exc:  # noqa: BLE001
            out["exc"] = repr(exc)

    if when == "pending":
        out["after_request"] = sessions.request_cancel(session.id)
    thread = threading.Thread(target=runner)
    thread.start()
    if when == "in_flight":
        assert (entered or llm.entered).wait(20), "điểm giữ chưa đạt tới"
        out["after_request"] = sessions.request_cancel(session.id)
    thread.join(60)
    assert not thread.is_alive()
    return session, sessions.get(session.id), out


def assert_cancelled(sessions: Any, session: Any, final: Any, out: dict[str, Any]) -> Any:
    assert "exc" not in out, out.get("exc")
    assert final.status is SessionStatus.CANCELLED
    assert final.stop_reason is StopReason.CANCELLED_BY_USER
    report = sessions.get_report(session.id)
    assert report is not None and report.status is ReportStatus.PARTIAL
    assert report.stop_reason is StopReason.CANCELLED_BY_USER
    assert sessions.evidence_store(session.id).verify_integrity()
    return report


@pytest.mark.parametrize(
    ("purpose", "nth", "evidence_expected"),
    [
        ("act", 1, False),  # A: hủy khi LLM chọn hành động lần 1, chưa có bằng chứng
        ("act", 2, True),  # B: đã có bằng chứng của bước 1
        ("plan", 1, False),  # C: hủy lúc lập kế hoạch (CSDL từ chối ghi kế hoạch)
    ],
)
def test_cancel_during_llm_call_returns_partial_report(sessions, make_orchestrator, purpose, nth, evidence_expected):
    llm = HookedMock(purpose, nth, hold=1.0)
    session, final, out = run_with_cancel(sessions, make_orchestrator(llm), llm, when="in_flight")
    assert out["after_request"].status is SessionStatus.CANCELLING
    report = assert_cancelled(sessions, session, final, out)
    assert report.generated_by == "extractive"
    assert "synthesize" not in llm.calls and "verify" not in llm.calls  # hủy => không gọi thêm LLM tổng hợp
    assert bool(len(sessions.evidence_store(session.id))) is evidence_expected
    assert any("hủy" in w for w in report.warnings)


def test_cancel_during_slow_synthesis_window_is_not_blocked_by_llm(sessions, make_orchestrator):
    """E: LLM tổng hợp chậm 3s/lần — hủy phải trả ngay, không chờ tổng hợp."""
    llm = HookedMock("act", 2, hold=1.0, synth_delay=3.0)
    started = time.monotonic()
    session, final, out = run_with_cancel(sessions, make_orchestrator(llm), llm, when="in_flight")
    assert time.monotonic() - started < 3.0
    assert_cancelled(sessions, session, final, out)
    assert "synthesize" not in llm.calls


def test_cancel_during_tool_execution(sessions, make_orchestrator):
    """F: hủy khi công cụ đang chạy."""
    entered = threading.Event()
    llm = HookedMock()
    orch = make_orchestrator(llm, wrap_search=lambda tool: SlowTool(tool, entered, 1.0))
    session, final, out = run_with_cancel(sessions, orch, llm, when="in_flight", entered=entered)
    report = assert_cancelled(sessions, session, final, out)
    assert report.generated_by == "extractive"
    steps = sessions.list_steps(session.id)
    assert steps and all(s.finished_at is not None for s in steps)


def test_cancel_pending_session_before_background_task_starts(sessions, make_orchestrator):
    """D/T4: phiên pending bị hủy -> cancelling ngay, run() chỉ ghi báo cáo đã hủy, không gọi LLM."""
    llm = HookedMock()
    session, final, out = run_with_cancel(sessions, make_orchestrator(llm), llm, when="pending")
    assert out["after_request"].status is SessionStatus.CANCELLING
    report = assert_cancelled(sessions, session, final, out)
    assert llm.calls == []
    assert report.generated_by == "extractive"
    assert sessions.list_steps(session.id) == []


def test_control_no_cancel_completes(sessions, make_orchestrator):
    llm = HookedMock()
    session = sessions.create(QUERY, Limits(10, 20000, 60))
    report = make_orchestrator(llm).run(session.id)
    final = sessions.get(session.id)
    assert final.status in (SessionStatus.COMPLETED, SessionStatus.BUDGET_EXHAUSTED)
    assert report.stop_reason is not StopReason.CANCELLED_BY_USER
    assert len(sessions.evidence_store(session.id)) >= 1
    assert sessions.evidence_store(session.id).verify_integrity()


def test_cancel_is_idempotent_and_terminal_session_unchanged(sessions, make_orchestrator):
    llm = HookedMock()
    session = sessions.create(QUERY, Limits(10, 20000, 60))
    make_orchestrator(llm).run(session.id)
    before = sessions.get(session.id)
    after = sessions.request_cancel(session.id)
    assert after.status is before.status
    assert sessions.request_cancel(session.id).status is before.status
