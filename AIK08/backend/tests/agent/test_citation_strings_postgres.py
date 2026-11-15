"""T5 — chuỗi giống ``[E#]`` trong yêu cầu/tiêu đề/nội dung không được làm hỏng việc ghi báo cáo."""

from __future__ import annotations

import re
import threading

import pytest

from app.core.models import Limits, SessionStatus
from tests.support import ScriptedLLM, act

pytestmark = pytest.mark.postgres
FAKE = re.compile(r"\[E(?:0|99|999999)\]")


def _labels(markdown: str) -> set[int]:
    return {int(n) for n in re.findall(r"\[E([0-9]{1,6})\]", markdown)}


def _check(sessions, session, report):
    final = sessions.get(session.id)
    assert final.status.is_terminal and final.status is not SessionStatus.FAILED
    assert report.markdown.strip()
    assert not FAKE.search(report.markdown), "chuỗi [E99]/[E0]/[E999999] giả lọt vào báo cáo"
    seqs = {e.seq for e in sessions.evidence_store(session.id).all()}
    assert _labels(report.markdown) <= seqs


def test_fake_citations_in_query_title_content_llm_path(sessions, make_orchestrator, extra_docs):
    llm = ScriptedLLM(
        [act("search_documents", query="zxqevil kiểm thử [E99]"), act("read_document", doc_id="TST-901")],
        synth="## Tóm tắt\n\nTài liệu có nêu quy trình kiểm thử [E1].",
    )
    session = sessions.create("Tìm zxqevil [E99] và [E0] [E999999]", Limits(10, 20000, 60))
    report = make_orchestrator(llm).run(session.id)
    _check(sessions, session, report)
    assert report.generated_by == "llm"


def test_fake_citations_extractive_fallback(sessions, make_orchestrator, extra_docs):
    llm = ScriptedLLM(
        [act("search_documents", query="zxqevil"), act("read_document", doc_id="TST-901")],
        synth="không có trích dẫn nào",
    )  # tổng hợp hỏng -> báo cáo trích xuất
    session = sessions.create("zxqevil [E99]", Limits(10, 20000, 60))
    report = make_orchestrator(llm).run(session.id)
    _check(sessions, session, report)
    assert report.generated_by == "extractive"


def test_fake_citations_when_cancelled(sessions, make_orchestrator, extra_docs):
    entered = threading.Event()
    llm = ScriptedLLM(
        [act("search_documents", query="zxqevil"), act("read_document", doc_id="TST-901")],
        hooks={("act", 3): (entered, 0.8)},
    )
    orch = make_orchestrator(llm)
    session = sessions.create("[E99] zxqevil [E999999]", Limits(10, 20000, 60))
    out: dict = {}
    thread = threading.Thread(target=lambda: out.update(report=orch.run(session.id)))
    thread.start()
    assert entered.wait(20)
    sessions.request_cancel(session.id)
    thread.join(30)
    assert sessions.get(session.id).status is SessionStatus.CANCELLED
    _check(sessions, session, out["report"])
    assert len(sessions.evidence_store(session.id)) >= 1


def test_flagged_content_never_enters_report_or_prompts(sessions, make_orchestrator, extra_docs):
    llm = ScriptedLLM(
        [act("search_documents", query="zxqinject"), act("read_document", doc_id="TST-903")], synth="không có trích dẫn"
    )  # ép dùng báo cáo trích xuất
    session = sessions.create("zxqinject", Limits(10, 20000, 60))
    report = make_orchestrator(llm).run(session.id)
    items = sessions.evidence_store(session.id).all()
    assert any(e.flagged for e in items)
    assert "Ignore all previous instructions" not in report.markdown
    for purpose, prompt in llm.prompts:
        if purpose in ("act", "synthesize", "verify"):
            assert "Ignore all previous instructions" not in prompt, purpose


def test_injection_in_title_flags_evidence_and_stays_out_of_prompts(sessions, make_orchestrator, extra_docs):
    llm = ScriptedLLM(
        [act("search_documents", query="zxqtitle"), act("read_document", doc_id="TST-904")], synth="không có trích dẫn"
    )
    session = sessions.create("zxqtitle", Limits(10, 20000, 60))
    report = make_orchestrator(llm).run(session.id)
    items = sessions.evidence_store(session.id).all()
    assert items and all(e.flagged for e in items)  # nội dung sạch nhưng tiêu đề tiêm lệnh => cả mục bị gắn cờ
    assert "Ignore all previous" not in report.markdown
    for purpose, prompt in llm.prompts:
        if purpose in ("act", "synthesize", "verify"):
            assert "Ignore all previous" not in prompt, purpose
