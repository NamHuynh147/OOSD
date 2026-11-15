"""2.3 — chất lượng tìm kiếm tiếng Việt trên PostgreSQL thật (không vector): recall@3 và từ chối câu hỏi ngoài phạm vi."""

import pytest

from tests.eval.search_cases import OUT_OF_SCOPE, RELEVANT

pytestmark = pytest.mark.postgres


def test_recall_at_3_on_vietnamese_questions(documents, capsys):
    misses = []
    for question, accepted in RELEVANT:
        top = [h.doc_id for h in documents.search(question, top_k=3)]
        if not accepted & set(top):
            misses.append((question, sorted(accepted), top))
    recall = 1 - len(misses) / len(RELEVANT)
    with capsys.disabled():
        print(f"\nrecall@3 = {recall:.0%} ({len(RELEVANT) - len(misses)}/{len(RELEVANT)})")
        for m in misses:
            print("  trượt:", m)
    assert len(RELEVANT) >= 30
    assert recall >= 0.9, misses


def test_out_of_scope_questions_return_nothing(documents, capsys):
    leaked = [(q, [h.doc_id for h in documents.search(q, top_k=3)]) for q in OUT_OF_SCOPE]
    leaked = [x for x in leaked if x[1]]
    with capsys.disabled():
        print(f"\nngoài phạm vi trả rỗng: {len(OUT_OF_SCOPE) - len(leaked)}/{len(OUT_OF_SCOPE)}")
        for item in leaked:
            print("  lọt:", item)
    assert len(leaked) <= 1, leaked


def test_hybrid_search_runs_with_reader_role_and_keeps_recall(documents_hybrid, capsys):
    """Hồi quy: vai trò chỉ-đọc phải thấy kiểu/toán tử vector (search_path gồm public)."""
    misses = [q for q, accepted in RELEVANT if not accepted & {h.doc_id for h in documents_hybrid.search(q, top_k=3)}]
    with capsys.disabled():
        print(f"\nrecall@3 (lai FTS+vector) = {1 - len(misses) / len(RELEVANT):.0%}")
    assert len(misses) <= 3, misses
