"""Read-only adapters over the PostgreSQL document repository."""

from __future__ import annotations

from typing import Any

from app.db.documents import DocumentRepository
from app.errors import InvalidToolArgumentsError
from app.tools.base import ToolResult

# read_document chỉ trả tối đa chừng này ký tự thân tài liệu: đủ cho báo cáo (tổng hợp cắt 1.500 ký tự
# mỗi bằng chứng) và không làm tràn ngân sách token của các lượt sau.
MAX_DOCUMENT_CHARS = 8_000


class DocumentSearchTool:
    name = "search_documents"
    description = "Tìm tài liệu liên quan trong kho tri thức nội bộ. Tham số: query (str), top_k (1–10). Chỉ đọc."

    def __init__(self, repository: DocumentRepository) -> None:
        self._repository = repository

    @staticmethod
    def validate(arguments: dict[str, Any]) -> tuple[str, int]:
        query = arguments.get("query")
        if not isinstance(query, str) or not query.strip() or len(query) > 2_000:
            raise InvalidToolArgumentsError("query phải là chuỗi không rỗng, tối đa 2.000 ký tự")
        top_k = arguments.get("top_k", 3)
        if isinstance(top_k, bool) or not isinstance(top_k, int) or not 1 <= top_k <= 10:
            raise InvalidToolArgumentsError("top_k phải là số nguyên từ 1 đến 10")
        return query.strip(), top_k

    def execute(self, arguments: dict[str, Any]) -> ToolResult:
        query, top_k = self.validate(arguments)
        hits = self._repository.search(query, top_k)
        data = [
            {
                "doc_id": h.doc_id,
                "title": h.title,
                "category": h.category,
                "source_uri": h.source_uri,
                "publisher": h.publisher,
                "content": h.snippet,
                "score": h.score,
            }
            for h in hits
        ]
        return ToolResult(self.name, data, f"Tìm thấy {len(hits)} tài liệu phù hợp.")


class ReadDocumentTool:
    name = "read_document"
    description = "Đọc toàn văn tài liệu theo doc_id. Tham số: doc_id (str). Chỉ đọc."

    def __init__(self, repository: DocumentRepository) -> None:
        self._repository = repository

    @staticmethod
    def validate(arguments: dict[str, Any]) -> str:
        doc_id = arguments.get("doc_id")
        if not isinstance(doc_id, str) or not doc_id.strip() or len(doc_id) > 128:
            raise InvalidToolArgumentsError("doc_id phải là chuỗi không rỗng, tối đa 128 ký tự")
        return doc_id.strip()

    def execute(self, arguments: dict[str, Any]) -> ToolResult:
        doc_id = self.validate(arguments)
        doc = self._repository.get(doc_id)
        if doc is None:
            return ToolResult(self.name, [], f"Không tìm thấy tài liệu {doc_id!r}.")
        truncated = len(doc.body) > MAX_DOCUMENT_CHARS
        body = doc.body[:MAX_DOCUMENT_CHARS] if truncated else doc.body
        note = f" (cắt còn {MAX_DOCUMENT_CHARS} trên {len(doc.body)} ký tự)" if truncated else ""
        return ToolResult(
            self.name,
            [
                {
                    "doc_id": doc.doc_id,
                    "title": doc.title,
                    "category": doc.category,
                    "source_uri": doc.source_uri,
                    "publisher": doc.publisher,
                    "published_at": doc.published_at.isoformat(),
                    "language": doc.language,
                    "content": body,
                    "truncated": truncated,
                }
            ],
            f"Đã đọc tài liệu {doc.title!r}{note}.",
        )
