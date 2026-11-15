"""2.1 — mọi bước của agent ghi span OpenTelemetry (kiểm bằng InMemorySpanExporter, PostgreSQL thật)."""

from __future__ import annotations

import pytest

from app.core.models import Limits
from app.telemetry.otel import configure_telemetry, shutdown_telemetry
from tests.support import FINISH, ScriptedLLM, act

pytestmark = pytest.mark.postgres


@pytest.fixture
def exporter():
    memory = configure_telemetry(in_memory=True)
    yield memory
    shutdown_telemetry()


def _names(exporter):
    return [s.name for s in exporter.get_finished_spans()]


def test_full_run_emits_all_span_kinds_and_nests_under_session(sessions, make_orchestrator, exporter):
    llm = ScriptedLLM([act("search_documents", query="sao lưu"), FINISH])
    session = sessions.create("quy định sao lưu thanh toán", Limits(10, 20000, 60))
    make_orchestrator(llm).run(session.id)
    names = _names(exporter)
    for expected in (
        "agent.session",
        "planner.plan",
        "llm.complete",
        "orchestrator.iteration",
        "guarded_tool.call",
        "tool.execute",
        "injection_guard.scan",
        "evidence.append",
        "report.synthesize",
        "rag.verify",
    ):
        assert expected in names, expected
    assert len(names) >= 8
    spans = exporter.get_finished_spans()
    root = next(s for s in spans if s.name == "agent.session")
    assert root.attributes["session.id"] == str(session.id) and root.attributes["report.generated_by"] == "llm"
    assert {s.context.trace_id for s in spans} == {root.context.trace_id}  # cùng một trace
    purposes = {s.attributes["llm.purpose"] for s in spans if s.name == "llm.complete"}
    assert {"plan", "act", "synthesize", "verify"} <= purposes


def test_blocked_tool_call_is_visible_as_decision_blocked_without_error_status(sessions, make_orchestrator, exporter):
    llm = ScriptedLLM([act("delete_all_documents"), FINISH])
    session = sessions.create("quy định sao lưu", Limits(10, 20000, 60))
    make_orchestrator(llm).run(session.id)
    calls = [s for s in exporter.get_finished_spans() if s.name == "guarded_tool.call"]
    blocked = [s for s in calls if s.attributes["decision"] == "blocked"]
    assert blocked and blocked[0].attributes["tool.requested"] == "delete_all_documents"
    assert blocked[0].status.is_ok or blocked[0].status.status_code.name == "UNSET"


def test_injection_scan_span_reports_flag(sessions, make_orchestrator, exporter, extra_docs):
    llm = ScriptedLLM([act("read_document", doc_id="TST-903"), FINISH])
    session = sessions.create("zxqinject", Limits(10, 20000, 60))
    make_orchestrator(llm).run(session.id)
    scans = [s for s in exporter.get_finished_spans() if s.name == "injection_guard.scan"]
    assert any(s.attributes["injection.flagged"] for s in scans)
