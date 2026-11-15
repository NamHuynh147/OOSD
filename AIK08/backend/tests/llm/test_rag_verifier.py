from datetime import UTC, datetime
from uuid import uuid4

from app.agent.report_synthesizer import ReportSynthesizer
from app.evidence.models import Evidence
from app.llm.provider import LLMResponse, MockLLMProvider


class ScriptedLLM:
    name = "test"
    model = "test-model"

    def __init__(self, verdict="supported"):
        self.verdict = verdict
        self.calls = []

    def complete(self, *, system, user, purpose):
        self.calls.append(purpose)
        if purpose == "synthesize":
            text = "## Báo cáo\n\nChính sách yêu cầu luân chuyển mật khẩu định kỳ [E1]."
        elif purpose == "verify":
            text = '{"verdict":"' + self.verdict + '","issues":[],"checked_citations":[1]}'
        else:
            text = "{}"
        return LLMResponse(text, self.name, self.model, 10, 10, 1)


def evidence(flagged=False):
    return Evidence(
        session_id=uuid4(),
        seq=1,
        step_no=1,
        tool_name="read_document",
        source_uri="doc://policy/password",
        title="Chính sách mật khẩu",
        content="Chính sách yêu cầu luân chuyển mật khẩu định kỳ để giảm nguy cơ lộ thông tin.",
        raw_sha256="a" * 64,
        content_sha256="b" * 64,
        prev_hash="c" * 64,
        chain_hash="d" * 64,
        flagged=flagged,
        findings=(),
        retrieved_at=datetime.now(UTC),
    )


def test_rag_verification_passes_only_with_supported_verdict():
    llm = ScriptedLLM("supported")
    draft, response = ReportSynthesizer(llm).synthesize("Chính sách mật khẩu", [evidence()])
    assert response is not None
    assert draft.generated_by == "llm"
    assert "Kiểm chứng RAG" in draft.markdown
    assert llm.calls == ["synthesize", "verify"]


def test_rag_verification_fails_closed_to_extractive_report():
    llm = ScriptedLLM("unsupported")
    draft, response = ReportSynthesizer(llm).synthesize("Chính sách mật khẩu", [evidence()])
    assert response is not None
    assert draft.generated_by == "extractive"
    assert any("RAG Verification không đạt" in warning for warning in draft.warnings)


def test_mock_provider_verification_is_verbatim_quote_matching_and_says_so():
    draft, _ = ReportSynthesizer(MockLLMProvider()).synthesize("Chính sách", [evidence()])
    assert draft.generated_by == "llm"
    assert "bộ kiểm chứng mock" in draft.markdown and "kiểm chứng ngữ nghĩa" in draft.markdown


# --- 1.11: bộ kiểm chứng phải thấy MỌI đoạn được trích dẫn ---------------------------------------
import json  # noqa: E402

from app.rag.retriever import retrieve_for_verification  # noqa: E402
from app.rag.verifier import RAGClaimVerifier  # noqa: E402


def make_evidence(seq, content, title="Tài liệu"):
    base = evidence()
    return Evidence(
        base.session_id,
        seq,
        seq,
        "read_document",
        f"doc://t/{seq}",
        f"{title} {seq}",
        content,
        "a" * 64,
        "b" * 64,
        "c" * 64,
        "d" * 64,
        False,
        (),
        base.retrieved_at,
    )


class RecordingVerifier:
    name, model = "rec", "rec"

    def __init__(self, bad_label=None):
        self.bad_label, self.batches = bad_label, []

    def complete(self, *, system, user, purpose, timeout_seconds=None):
        payload = json.loads(user)
        labels = [int(p["label"][1:]) for p in payload["retrieved_evidence"]]
        self.batches.append((payload["must_check_citations"], labels))
        verdict = "unsupported" if self.bad_label in payload["must_check_citations"] else "supported"
        text = json.dumps({"verdict": verdict, "issues": [], "checked_citations": payload["must_check_citations"]})
        return LLMResponse(text, "rec", "rec", 10, 5, 1)


def test_cited_passage_is_always_retrieved_even_with_zero_overlap_and_many_distractors():
    ev = [make_evidence(1, "nội dung hoàn toàn khác biệt xyz")] + [
        make_evidence(n, "chính sách mật khẩu luân chuyển định kỳ bảo mật") for n in range(2, 14)
    ]
    passages = retrieve_for_verification("chính sách mật khẩu", "Có luân chuyển mật khẩu định kỳ [E1].", ev)
    assert "E1" in {p.label for p in passages}


def test_twelve_citations_are_checked_in_batches_of_eight_and_all_seen():
    ev = [make_evidence(n, f"nội dung số {n} về mật khẩu") for n in range(1, 13)]
    report = "## B\n\n" + " ".join(f"Ý {n} [E{n}]." for n in range(1, 13))
    llm = RecordingVerifier()
    result = RAGClaimVerifier(llm).verify("mật khẩu", report, ev)
    assert result.passed and len(llm.batches) == 2
    seen = {n for must, labels in llm.batches for n in labels}
    assert set(range(1, 13)) <= seen
    assert [len(must) for must, _ in llm.batches] == [8, 4]
    assert result.response is not None and result.response.input_tokens == 20


def test_one_failing_batch_fails_the_whole_report():
    ev = [make_evidence(n, f"nội dung số {n} về mật khẩu") for n in range(1, 13)]
    report = "## B\n\n" + " ".join(f"Ý {n} [E{n}]." for n in range(1, 13))
    result = RAGClaimVerifier(RecordingVerifier(bad_label=11)).verify("mật khẩu", report, ev)
    assert not result.passed
