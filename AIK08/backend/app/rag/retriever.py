"""Small deterministic retrieval layer over immutable session evidence.

The database document search already uses hybrid full-text/vector retrieval. This module
performs a second retrieval pass over evidence collected for the current run so the
verifier receives only passages relevant to the draft's claims.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from app.core.text import significant_terms
from app.evidence.models import Evidence


@dataclass(frozen=True, slots=True)
class RetrievedPassage:
    label: str
    title: str
    source_uri: str
    content: str
    score: float


def _terms(text: str) -> set[str]:
    return set(significant_terms(text))


def cited_labels(report: str) -> set[int]:
    return {int(n) for n in re.findall(r"\[E(\d{1,6})\]", report)}


def retrieve_for_verification(
    query: str,
    report: str,
    evidence: tuple[Evidence, ...] | list[Evidence],
    *,
    top_k: int = 8,
) -> list[RetrievedPassage]:
    """Chọn đoạn bằng chứng đưa cho bộ kiểm chứng.

    * MỌI đoạn được báo cáo trích dẫn (và không bị gắn cờ) luôn có mặt, bất kể điểm xếp hạng: bộ kiểm
      chứng không thể xác nhận một nhận định mà không thấy nguồn của nó.
    * Các đoạn không được trích dẫn chỉ bổ sung tối đa ``top_k`` đoạn có điểm trùng từ cao nhất, làm ngữ cảnh.
    Bằng chứng bị gắn cờ prompt injection không bao giờ được đưa vào.
    """
    cited = cited_labels(report)
    claim_text = " ".join(line for line in report.splitlines() if line.strip() and not line.lstrip().startswith("#"))
    query_terms = _terms(query + " " + claim_text)
    must: list[RetrievedPassage] = []
    extra: list[RetrievedPassage] = []
    for item in evidence:
        if item.flagged:
            continue
        content_terms = _terms(item.title + " " + item.content)
        score = len(query_terms & content_terms) / max(1, len(query_terms)) if content_terms else 0.0
        passage = RetrievedPassage(item.label, item.title, item.source_uri, item.content[:1800], score)
        if item.seq in cited:
            must.append(passage)
        elif score > 0:
            extra.append(passage)
    must.sort(key=lambda p: int(p.label[1:]))
    extra.sort(key=lambda p: (-p.score, p.label))
    return must + extra[: max(0, min(top_k, 10))]
