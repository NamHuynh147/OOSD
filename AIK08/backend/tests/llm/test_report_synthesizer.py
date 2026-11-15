from datetime import UTC, datetime
from uuid import uuid4

from app.agent.report_synthesizer import ReportSynthesizer
from app.evidence.models import Evidence
from app.llm.provider import MockLLMProvider


def test_synthesizer_without_evidence_returns_explicit_no_evidence_report():
    draft, response = ReportSynthesizer(MockLLMProvider()).synthesize("Tìm quy định", [])
    assert response is None
    assert draft.generated_by == "extractive"
    assert "Chưa thu thập được bằng chứng" in draft.markdown


def test_synthesizer_uses_llm_for_evidence():
    item = Evidence(
        session_id=uuid4(),
        seq=1,
        step_no=1,
        tool_name="search_documents",
        source_uri="doc://policy/one",
        title="Chính sách",
        content="Quy trình kiểm soát truy cập.",
        raw_sha256="a" * 64,
        content_sha256="b" * 64,
        prev_hash="c" * 64,
        chain_hash="d" * 64,
        flagged=False,
        findings=(),
        retrieved_at=datetime.now(UTC),
    )
    draft, response = ReportSynthesizer(MockLLMProvider()).synthesize("Tìm quy định", [item])
    # Mock chỉ trích nguyên văn và tự kiểm bằng đối chiếu chuỗi: báo cáo có trích dẫn, qua kiểm chứng, và nói rõ là mock.
    assert response is not None and draft.generated_by == "llm"
    assert "«Quy trình kiểm soát truy cập.» [E1]" in draft.markdown
    assert "bộ kiểm chứng mock" in draft.markdown


def test_mock_verifier_rejects_a_quote_that_is_not_in_the_cited_evidence():
    from app.rag.verifier import RAGClaimVerifier

    item = Evidence(
        session_id=uuid4(),
        seq=1,
        step_no=1,
        tool_name="search_documents",
        source_uri="doc://p/1",
        title="Chính sách",
        content="Quy trình kiểm soát truy cập.",
        raw_sha256="a" * 64,
        content_sha256="b" * 64,
        prev_hash="c" * 64,
        chain_hash="d" * 64,
        flagged=False,
        findings=(),
        retrieved_at=datetime.now(UTC),
    )
    forged = "## B\n\n- «Mật khẩu hết hạn sau 30 ngày» [E1]"
    assert not RAGClaimVerifier(MockLLMProvider()).verify("q", forged, [item]).passed
