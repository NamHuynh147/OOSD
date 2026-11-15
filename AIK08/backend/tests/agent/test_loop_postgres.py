"""T6/T7 — quyết định sai của LLM, lặp, ngân sách bước/thời gian, tài liệu rất dài (PostgreSQL thật)."""

from __future__ import annotations

import time

import pytest

from app.core.models import Limits, SessionStatus, StepDecision, StopReason
from app.errors import LLMError
from tests.support import FINISH, ScriptedLLM, act

pytestmark = pytest.mark.postgres


def _run(sessions, make_orchestrator, llm, query="quy định sao lưu thanh toán", limits=Limits(10, 20000, 60), **kw):
    session = sessions.create(query, limits)
    report = make_orchestrator(llm, **kw).run(session.id)
    return session, report, sessions.list_steps(session.id), sessions.get(session.id)


def test_unknown_tool_is_recorded_as_blocked_policy_then_llm_can_recover(sessions, make_orchestrator):
    llm = ScriptedLLM([act("delete_all_documents", id=1), act("search_documents", query="sao lưu"), FINISH])
    _, report, steps, final = _run(sessions, make_orchestrator, llm)
    blocked = [s for s in steps if s.decision is StepDecision.BLOCKED_POLICY]
    assert len(blocked) == 1 and blocked[0].tool_name is None and blocked[0].requested_tool == "delete_all_documents"
    assert any(s.decision is StepDecision.EXECUTED for s in steps)
    assert final.status is SessionStatus.COMPLETED and report.stop_reason is StopReason.ENOUGH_EVIDENCE
    assert llm.counts["act"] == 3  # LLM được hỏi lại sau khi bị từ chối


def test_three_consecutive_violations_stop_with_policy_violations(sessions, make_orchestrator):
    llm = ScriptedLLM([act("rm_rf"), "đây không phải JSON", act("drop_table")])
    _, report, steps, final = _run(sessions, make_orchestrator, llm)
    assert [s.decision for s in steps] == [StepDecision.BLOCKED_POLICY] * 3
    assert report.stop_reason is StopReason.POLICY_VIOLATIONS and final.status is SessionStatus.FAILED
    assert report.markdown.strip()  # vẫn có báo cáo dù không có bằng chứng


def test_invalid_arguments_recorded_and_counted(sessions, make_orchestrator):
    llm = ScriptedLLM([act("search_documents"), act("search_documents", query=""), act("read_document", doc_id=123)])
    _, report, steps, _ = _run(sessions, make_orchestrator, llm)
    assert [s.decision for s in steps] == [StepDecision.INVALID_ARGUMENTS] * 3
    assert all(s.tool_name == "search_documents" or s.requested_tool == "read_document" for s in steps)
    assert report.stop_reason is StopReason.POLICY_VIOLATIONS


def test_valid_step_resets_violation_counter(sessions, make_orchestrator):
    llm = ScriptedLLM([act("rm"), act("rm"), act("search_documents", query="sao lưu"), act("rm"), act("rm"), FINISH])
    _, report, steps, _ = _run(sessions, make_orchestrator, llm)
    assert report.stop_reason is StopReason.ENOUGH_EVIDENCE
    assert sum(s.decision is StepDecision.BLOCKED_POLICY for s in steps) == 4


def test_duplicate_action_recorded_then_stops_as_enough_evidence(sessions, make_orchestrator):
    same = act("search_documents", query="sao lưu thanh toán")
    llm = ScriptedLLM([same, same, same])
    _, report, steps, final = _run(sessions, make_orchestrator, llm)
    decisions = [s.decision for s in steps]
    assert decisions == [StepDecision.EXECUTED, StepDecision.DUPLICATE, StepDecision.DUPLICATE]
    assert report.stop_reason is StopReason.ENOUGH_EVIDENCE and final.status is SessionStatus.COMPLETED


def test_max_steps_one_still_produces_report(sessions, make_orchestrator):
    llm = ScriptedLLM([act("search_documents", query="sao lưu"), act("search_documents", query="khác")])
    _, report, steps, final = _run(sessions, make_orchestrator, llm, limits=Limits(1, 20000, 60))
    assert len(steps) == 1 and steps[0].decision is StepDecision.EXECUTED
    assert report.markdown.strip() and final.status.is_terminal
    assert final.usage.steps == 1


def test_ten_distinct_tool_calls_all_execute_within_ten_step_budget(sessions, make_orchestrator):
    queries = [
        "sao lưu",
        "phục hồi",
        "sự cố",
        "SLA",
        "mật khẩu",
        "truy cập",
        "canary",
        "thay đổi",
        "kiến trúc",
        "thanh toán",
    ]
    llm = ScriptedLLM([act("search_documents", query=q) for q in queries] + [FINISH])
    _, report, steps, final = _run(sessions, make_orchestrator, llm, limits=Limits(10, 50000, 60))
    assert [s.decision for s in steps] == [StepDecision.EXECUTED] * 10  # không bị tính đôi
    assert final.usage.steps == 10
    assert report.stop_reason in (StopReason.ENOUGH_EVIDENCE, StopReason.BUDGET_STEPS)


def test_time_budget_is_enforced_by_llm_timeout_and_report_is_still_written(sessions, make_orchestrator):
    llm = ScriptedLLM([act("search_documents", query="sao lưu")], delays={"act": 30.0})
    started = time.monotonic()
    _, report, steps, final = _run(sessions, make_orchestrator, llm, limits=Limits(10, 20000, 5))
    elapsed = time.monotonic() - started
    assert elapsed < 12, f"phiên 5s chạy {elapsed:.1f}s"
    assert final.status.is_terminal and report.markdown.strip()
    assert "synthesize" not in llm.counts  # còn quá ít thời gian: bỏ lời gọi tổng hợp


def test_llm_error_in_act_stops_with_error_and_report(sessions, make_orchestrator):
    llm = ScriptedLLM([act("search_documents", query="sao lưu"), LLMError("nhà cung cấp lỗi")])
    _, report, steps, final = _run(sessions, make_orchestrator, llm)
    assert final.status is SessionStatus.FAILED and report.stop_reason is StopReason.ERROR
    assert len(steps) == 1 and report.markdown.strip()


def test_very_long_document_is_truncated_not_fatal(sessions, make_orchestrator, extra_docs):
    llm = ScriptedLLM([act("read_document", doc_id="TST-902"), FINISH], synth="## Tóm tắt\n\nTài liệu dài [E1].")
    session, report, steps, final = _run(sessions, make_orchestrator, llm, query="zxqlong")
    items = sessions.evidence_store(session.id).all()
    assert len(items) == 1 and len(items[0].content) <= 8000
    assert final.status is SessionStatus.COMPLETED
    assert sessions.evidence_store(session.id).verify_integrity()
    sizes = [len(p) for purpose, p in llm.prompts if purpose in ("act", "synthesize", "verify")]
    assert max(sizes) < 30_000  # prompt không phình theo tài liệu 63.000 ký tự


def test_defence_in_depth_when_llm_obeys_an_injection_the_guard_missed(sessions, make_orchestrator):
    """Luật quét chỉ là tín hiệu (xem docs/05): khi một lệnh tiêm lọt và LLM làm theo, chính sách công cụ vẫn chặn.

    LLM giả lập "tuân lệnh" các chỉ thị lọt ở lô C: gọi công cụ ghi/xóa, đọc tệp và gọi API ngoài allowlist.
    Không hành động nào được thực thi; phiên vẫn kết thúc bằng báo cáo."""
    llm = ScriptedLLM(
        [
            act("delete_user", id=1),
            act("write_file", path="/tmp/x", content="secrets"),
            act("search_documents", query="sao lưu"),  # một bước hợp lệ xen giữa để chuỗi vi phạm không đạt 3 liên tiếp
            act("http_get_api", url="http://192.168.1.10/admin/export"),
            FINISH,
        ]
    )
    _, report, steps, final = _run(sessions, make_orchestrator, llm, limits=Limits(10, 20000, 60))
    by_tool = {s.requested_tool: s.decision for s in steps}
    assert by_tool["delete_user"] is StepDecision.BLOCKED_POLICY
    assert by_tool["write_file"] is StepDecision.BLOCKED_POLICY
    assert by_tool["http_get_api"] is StepDecision.BLOCKED_POLICY  # không nằm trong tập công cụ được cấp
    executed = [s.requested_tool for s in steps if s.decision is StepDecision.EXECUTED]
    assert executed == ["search_documents"]
    assert final.status in (SessionStatus.COMPLETED, SessionStatus.FAILED) and report is not None
