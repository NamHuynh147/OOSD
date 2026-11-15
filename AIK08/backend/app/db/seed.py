"""Nạp kho tài liệu mẫu vào aik08.documents (vai trò OWNER, idempotent).

    python -m app.db.seed

Tài liệu nằm ở app/data/corpus/*.md; front-matter ánh xạ thẳng sang cột của bảng ``documents``:

    ---
    id: POL-001                      # doc_id   (ck_documents_doc_id)
    category: policy                 # FK -> document_categories
    title: Chính sách mật khẩu
    publisher: Quy chế ATTT v3.2     # đơn vị ban hành (provenance)
    published: 2026-01-15
    ---
    <nội dung>

``source_uri`` được sinh là ``doc://<category>/<tên-tệp>``. Mọi quy tắc dữ liệu (định dạng mã,
độ dài, URI hợp lệ...) do CSDL kiểm tra; seed không tự kiểm lại.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import psycopg

from app.config import Settings
from app.errors import ConfigurationError
from app.llm.embeddings import EmbeddingProvider, HashingEmbedder, to_pgvector

CORPUS_DIR = Path(__file__).resolve().parent.parent / "data" / "corpus"
_FRONT_MATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n(.*)\Z", re.DOTALL)

CATEGORY_LABELS = {
    "policy": "Chính sách",
    "process": "Quy trình",
    "sla": "Cam kết dịch vụ",
    "architecture": "Kiến trúc",
    "report": "Báo cáo",
    "continuity": "Liên tục hoạt động",
    "note": "Ghi chú",
}


@dataclass(frozen=True, slots=True)
class CorpusDocument:
    doc_id: str
    category: str
    title: str
    publisher: str
    published_at: date
    source_uri: str
    body: str


def parse_document(path: Path) -> CorpusDocument:
    match = _FRONT_MATTER.match(path.read_text(encoding="utf-8"))
    if not match:
        raise ConfigurationError(f"{path.name}: thiếu front-matter '---'")
    meta: dict[str, str] = {}
    for line in match.group(1).splitlines():
        key, sep, value = line.partition(":")
        if sep:
            meta[key.strip()] = value.strip()
    for required in ("id", "category", "title", "published"):
        if not meta.get(required):
            raise ConfigurationError(f"{path.name}: thiếu trường '{required}'")
    category = meta["category"]
    if category not in CATEGORY_LABELS:
        raise ConfigurationError(
            f"{path.name}: nhóm '{category}' chưa có nhãn trong CATEGORY_LABELS"
        )
    return CorpusDocument(
        doc_id=meta["id"],
        category=category,
        title=meta["title"],
        publisher=meta.get("publisher", ""),
        published_at=date.fromisoformat(meta["published"]),
        source_uri=f"doc://{category}/{path.stem}",
        body=match.group(2).strip(),
    )


def load_corpus(directory: Path = CORPUS_DIR) -> list[CorpusDocument]:
    return [parse_document(p) for p in sorted(directory.glob("*.md"))]


_UPSERT_CATEGORY = """
INSERT INTO aik08.document_categories (code, label) VALUES (%s, %s)
ON CONFLICT (code) DO UPDATE SET label = EXCLUDED.label
"""

_UPSERT_DOCUMENT = """
INSERT INTO aik08.documents (doc_id, category, title, body, source_uri, publisher, published_at)
VALUES (%(doc_id)s, %(category)s, %(title)s, %(body)s, %(source_uri)s, %(publisher)s, %(published_at)s)
ON CONFLICT (doc_id) DO UPDATE
   SET category = EXCLUDED.category, title = EXCLUDED.title, body = EXCLUDED.body,
       source_uri = EXCLUDED.source_uri, publisher = EXCLUDED.publisher,
       published_at = EXCLUDED.published_at, updated_at = now()
"""

_HAS_EMBEDDING = """
SELECT EXISTS (
    SELECT 1 FROM pg_attribute
     WHERE attrelid = 'aik08.documents'::regclass AND attname = 'embedding' AND NOT attisdropped
)
"""


def seed(
    owner_dsn: str,
    embedder: EmbeddingProvider | None = None,
    directory: Path = CORPUS_DIR,
) -> int:
    """Upsert danh mục + tài liệu (+ embedding nếu CSDL có cột vector). Trả về số tài liệu."""
    embedder = embedder or HashingEmbedder()
    docs = load_corpus(directory)
    with psycopg.connect(owner_dsn) as conn, conn.transaction():
        has_vector = bool(conn.execute(_HAS_EMBEDDING).fetchone()[0])  # type: ignore[index]
        for category in sorted({d.category for d in docs}):
            conn.execute(_UPSERT_CATEGORY, (category, CATEGORY_LABELS[category]))
        for doc in docs:
            conn.execute(
                _UPSERT_DOCUMENT,
                {
                    "doc_id": doc.doc_id,
                    "category": doc.category,
                    "title": doc.title,
                    "body": doc.body,
                    "source_uri": doc.source_uri,
                    "publisher": doc.publisher,
                    "published_at": doc.published_at,
                },
            )
            if has_vector:
                vector = embedder.embed(f"{doc.title}\n{doc.body}")
                conn.execute(
                    "UPDATE aik08.documents SET embedding = %s::vector WHERE doc_id = %s",
                    (to_pgvector(vector) if vector else None, doc.doc_id),
                )
    return len(docs)


def main() -> int:
    print(f"Đã nạp {seed(Settings.from_env().owner_dsn)} tài liệu vào aik08.documents.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
