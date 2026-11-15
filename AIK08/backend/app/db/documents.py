"""Nguồn tài liệu CHỈ ĐỌC: giao diện ``DocumentRepository`` + cài đặt PostgreSQL.

Cài đặt này chỉ nhận pool của vai trò ``aik08_reader`` (SELECT-only, giao dịch mặc định read-only,
statement_timeout 5s). Nhờ vậy công cụ tra cứu *không có đường nào* tới câu lệnh ghi — kể cả khi mã
ứng dụng có lỗi. Thêm nguồn mới = viết một adapter công cụ mới, không sửa orchestrator.

Tìm kiếm lai, tính hoàn toàn trong CSDL bằng SQL thuần:
  * toàn văn không dấu: ``ts_rank_cd(fts, to_tsquery('simple', ...), 32)``  (cột sinh ``fts`` + fold_vi);
  * vector (nếu có pgvector, cột ``embedding``): ``1 - (embedding <=> :vec)`` (cosine).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Protocol

from app.core.text import best_sentences, keywords, split_sentences, truncate
from app.db.errors import translate_errors
from app.db.pool import Database
from app.errors import ConfigurationError
from app.llm.embeddings import EmbeddingProvider, HashingEmbedder, to_pgvector

FTS_WEIGHT = 0.6
VECTOR_WEIGHT = 0.4
MIN_VECTOR_SCORE = 0.12  # dưới ngưỡng này coi như không liên quan
RELATIVE_CUTOFF = 0.6  # bỏ kết quả có điểm < 60% điểm của kết quả tốt nhất
MAX_TOP_K = 10


def min_matched_terms(n_terms: int) -> int:
    """Ngưỡng liên quan: số từ khóa tối thiểu một tài liệu phải chứa (>= 60%, làm tròn lên; 1-2 từ thì cần đủ).

    Chỉ mục toàn văn đã bỏ dấu nên "công" khớp "cổng", "gia" khớp "gia hạn": một hai từ trùng ngẫu nhiên đủ để
    nhồi tài liệu không liên quan cho câu hỏi ngoài phạm vi. Ngưỡng này loại các trường hợp đó.
    """
    return 1 if n_terms <= 1 else n_terms if n_terms == 2 else -(-n_terms * 6 // 10)


@dataclass(frozen=True, slots=True)
class Document:
    doc_id: str
    title: str
    category: str
    source_uri: str
    publisher: str
    published_at: date
    language: str
    body: str


@dataclass(frozen=True, slots=True)
class DocumentHit:
    doc_id: str
    title: str
    category: str
    source_uri: str
    publisher: str
    snippet: str
    score: float


class DocumentRepository(Protocol):
    """Giao diện CHỈ ĐỌC — cố ý không có phương thức ghi nào."""

    def search(self, query: str, top_k: int = 3) -> list[DocumentHit]: ...

    def get(self, doc_id: str) -> Document | None: ...


def make_snippet(
    body: str, terms: list[str], *, max_sentences: int = 3, max_chars: int = 600
) -> str:
    """Các câu khớp từ khóa nhất (giữ thứ tự gốc); không khớp thì lấy vài câu đầu."""
    chosen = best_sentences(body, terms, limit=max_sentences) if terms else []
    if not chosen:
        chosen = split_sentences(body)[:max_sentences]
    return truncate("\n".join(chosen) if chosen else body.strip(), max_chars)


class PostgresDocumentRepository:
    def __init__(
        self,
        db: Database,
        embedder: EmbeddingProvider | None = None,
        vector_mode: str = "auto",
    ) -> None:
        if vector_mode not in ("auto", "on", "off"):
            raise ConfigurationError(
                f"VECTOR_SEARCH phải là auto|on|off, nhận {vector_mode!r}"
            )
        self._db = db
        self._embedder = embedder or HashingEmbedder()
        present = self._embedding_column_exists()
        if vector_mode == "on" and not present:
            raise ConfigurationError(
                "VECTOR_SEARCH=on nhưng bảng documents chưa có cột embedding "
                "(cần pgvector: chạy migration 005_pgvector.optional.sql bằng siêu người dùng)."
            )
        self.vector_enabled = present and vector_mode != "off"

    def _embedding_column_exists(self) -> bool:
        with translate_errors(), self._db.reader() as conn:
            row = conn.execute(
                "SELECT EXISTS (SELECT 1 FROM pg_attribute WHERE attrelid = 'aik08.documents'::regclass "
                "AND attname = 'embedding' AND NOT attisdropped) AS present"
            ).fetchone()
        return bool(row and row["present"])

    def search(self, query: str, top_k: int = 3) -> list[DocumentHit]:
        top_k = max(1, min(int(top_k), MAX_TOP_K))
        terms = keywords(query)
        vector = self._embedder.embed(query) if self.vector_enabled else None
        if not terms and vector is None:
            return []

        params: dict[str, object] = {"k": top_k}
        if terms:
            fts_expr = "ts_rank_cd(d.fts, to_tsquery('simple', %(tsq)s), 32)"
            params["tsq"] = " | ".join(
                terms
            )  # token chỉ gồm [a-z0-9], an toàn với cú pháp tsquery
            params["terms"] = terms
        else:
            fts_expr = "0.0"
        if vector is not None:
            vec_expr = "GREATEST(0, 1 - (d.embedding <=> %(vec)s::vector))"
            params["vec"] = to_pgvector(vector)
        else:
            vec_expr = "0.0"
        fts_w, vec_w = (FTS_WEIGHT, VECTOR_WEIGHT) if vector is not None else (1.0, 0.0)
        params["min_vec"] = MIN_VECTOR_SCORE
        params["min_matched"] = min_matched_terms(len(terms))
        matched_expr = (
            "(SELECT count(*) FROM unnest(%(terms)s::text[]) AS q(term) WHERE d.fts @@ to_tsquery('simple', q.term))"
            if terms
            else "0"
        )

        sql = f"""
            SELECT s.*, ({fts_w} * s.fts_score + {vec_w} * s.vec_score) AS score
              FROM (
                    SELECT d.doc_id, d.title, d.category, d.source_uri, d.publisher, d.body,
                           {fts_expr} AS fts_score, {vec_expr} AS vec_score, {matched_expr} AS matched
                      FROM aik08.documents d
                   ) s
             WHERE s.matched >= %(min_matched)s OR s.vec_score > %(min_vec)s
             ORDER BY score DESC, s.doc_id
             LIMIT %(k)s
        """  # noqa: S608 — chỉ nối biểu thức cố định; mọi giá trị đi qua tham số
        with translate_errors(), self._db.reader() as conn:
            rows = conn.execute(sql, params).fetchall()
        if rows:
            best = float(rows[0]["score"])
            rows = [r for r in rows if float(r["score"]) >= RELATIVE_CUTOFF * best]
        return [
            DocumentHit(
                doc_id=r["doc_id"],
                title=r["title"],
                category=r["category"],
                source_uri=r["source_uri"],
                publisher=r["publisher"],
                snippet=make_snippet(r["body"], terms),
                score=round(float(r["score"]), 4),
            )
            for r in rows
        ]

    def get(self, doc_id: str) -> Document | None:
        with translate_errors(), self._db.reader() as conn:
            row = conn.execute(
                "SELECT doc_id, title, category, source_uri, publisher, published_at, language, body "
                "FROM aik08.documents WHERE doc_id = %s",
                (doc_id,),
            ).fetchone()
        return Document(**row) if row else None
