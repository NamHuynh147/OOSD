from typing import Any

import asyncpg

from app.evidence.models import Evidence
from app.tools.base import ReadOnlyTool


class DocumentSearchTool(ReadOnlyTool):
    name = "document_search"

    def __init__(self, pool: asyncpg.Pool) -> None:
        self.pool = pool

    async def execute(self, arguments: dict[str, Any]) -> tuple[Evidence, ...]:
        query = str(arguments.get("query", "")).strip()
        if not query:
            raise ValueError("Document search requires a non-empty query.")
        rows = await self.pool.fetch(
            """
            SELECT s.display_name, c.text
            FROM document_chunks AS c
            JOIN sources AS s ON s.id = c.source_id
            WHERE s.enabled = TRUE AND c.text ILIKE '%' || $1 || '%'
            ORDER BY s.display_name, c.position
            LIMIT 10
            """,
            query,
        )
        return tuple(Evidence.create(source=row["display_name"], content=row["text"]) for row in rows)
