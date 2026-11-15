"""EvidenceStore — bằng chứng chỉ được THÊM, không sửa, không xóa.

Cài đặt:
  * ``PostgresEvidenceStore`` — ghi vào ``aik08.evidence``. Số E#, băm nội dung và chuỗi băm do TRIGGER
    của CSDL tính nên ứng dụng không giả mạo được; bảng bị chặn UPDATE/DELETE/TRUNCATE bằng trigger
    (kể cả với chủ sở hữu) và không cấp quyền UPDATE/DELETE cho vai trò ứng dụng.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol
from uuid import UUID

from psycopg.types.json import Jsonb

from app.core.text import truncate
from app.db.errors import translate_errors
from app.db.pool import Database
from app.evidence.models import Evidence, EvidenceDraft, Finding, IntegrityReport

MAX_CONTENT_CHARS = 20_000  # khớp ck_evidence_content
MAX_TITLE_CHARS = 500  # khớp ck_evidence_title


class EvidenceStore(Protocol):
    """Giao diện cố tình KHÔNG có update / delete / clear."""

    def append(self, drafts: Sequence[EvidenceDraft], *, step_no: int) -> tuple[Evidence, ...]: ...

    def all(self) -> tuple[Evidence, ...]: ...

    def get(self, seq: int) -> Evidence | None: ...

    def __len__(self) -> int: ...

    def verify_integrity(self) -> IntegrityReport: ...


def _normalize(draft: EvidenceDraft) -> EvidenceDraft:
    """Đưa bản nháp vào giới hạn của CHECK (tiêu đề không rỗng, nội dung ≤ 20.000 ký tự)."""
    title = truncate(draft.title.strip() or draft.source_uri, MAX_TITLE_CHARS)
    content = truncate(draft.content, MAX_CONTENT_CHARS)
    return EvidenceDraft(
        tool_name=draft.tool_name,
        source_uri=draft.source_uri,
        title=title,
        content=content,
        raw_sha256=draft.raw_sha256,
        flagged=draft.flagged,
        findings=draft.findings,
    )


_INSERT = """
INSERT INTO aik08.evidence (session_id, step_no, source_uri, title, content, raw_sha256, flagged, findings)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
RETURNING seq, content_sha256, prev_hash, chain_hash, retrieved_at
"""

_SELECT = """
SELECT e.session_id, e.seq, e.step_no, s.tool_name, e.source_uri, e.title, e.content,
       e.raw_sha256, e.content_sha256, e.prev_hash, e.chain_hash, e.flagged, e.findings, e.retrieved_at
  FROM aik08.evidence e
  LEFT JOIN aik08.steps s ON s.session_id = e.session_id AND s.step_no = e.step_no
 WHERE e.session_id = %s
"""


def row_to_evidence(row: dict[str, object]) -> Evidence:
    return Evidence(
        session_id=row["session_id"],  # type: ignore[arg-type]
        seq=int(row["seq"]),  # type: ignore[arg-type]
        step_no=int(row["step_no"]),  # type: ignore[arg-type]
        tool_name=str(row["tool_name"] or ""),
        source_uri=str(row["source_uri"]),
        title=str(row["title"]),
        content=str(row["content"]),
        raw_sha256=str(row["raw_sha256"]),
        content_sha256=str(row["content_sha256"]),
        prev_hash=str(row["prev_hash"]),
        chain_hash=str(row["chain_hash"]),
        flagged=bool(row["flagged"]),
        findings=tuple(Finding.from_dict(f) for f in row["findings"]),  # type: ignore[attr-defined]
        retrieved_at=row["retrieved_at"],  # type: ignore[arg-type]
    )


class PostgresEvidenceStore:
    def __init__(self, db: Database, session_id: UUID) -> None:
        self._db = db
        self._session_id = session_id

    def append(self, drafts: Sequence[EvidenceDraft], *, step_no: int) -> tuple[Evidence, ...]:
        """Ghi cả lô trong MỘT giao dịch: hoặc đủ, hoặc không có gì."""
        added: list[Evidence] = []
        with translate_errors(), self._db.app() as conn, conn.transaction():
            for raw in drafts:
                d = _normalize(raw)
                row = conn.execute(
                    _INSERT,
                    (
                        self._session_id,
                        step_no,
                        d.source_uri,
                        d.title,
                        d.content,
                        d.raw_sha256,
                        d.flagged,
                        Jsonb([f.to_dict() for f in d.findings]),
                    ),
                ).fetchone()
                assert row is not None
                added.append(
                    Evidence(
                        session_id=self._session_id,
                        seq=row["seq"],
                        step_no=step_no,
                        tool_name=d.tool_name,
                        source_uri=d.source_uri,
                        title=d.title,
                        content=d.content,
                        raw_sha256=d.raw_sha256,
                        content_sha256=row["content_sha256"],
                        prev_hash=row["prev_hash"],
                        chain_hash=row["chain_hash"],
                        flagged=d.flagged,
                        findings=d.findings,
                        retrieved_at=row["retrieved_at"],
                    )
                )
        return tuple(added)

    def all(self) -> tuple[Evidence, ...]:
        with translate_errors(), self._db.app() as conn:
            rows = conn.execute(_SELECT + " ORDER BY e.seq", (self._session_id,)).fetchall()
        return tuple(row_to_evidence(r) for r in rows)

    def get(self, seq: int) -> Evidence | None:
        with translate_errors(), self._db.app() as conn:
            row = conn.execute(_SELECT + " AND e.seq = %s", (self._session_id, seq)).fetchone()
        return row_to_evidence(row) if row else None

    def __len__(self) -> int:
        with translate_errors(), self._db.app() as conn:
            row = conn.execute(
                "SELECT count(*) AS n FROM aik08.evidence WHERE session_id = %s", (self._session_id,)
            ).fetchone()
        return int(row["n"]) if row else 0

    def verify_integrity(self) -> IntegrityReport:
        """Gọi hàm SQL ``aik08.verify_evidence_chain`` — tính lại chuỗi băm ngay trong CSDL."""
        with translate_errors(), self._db.app() as conn:
            rows = conn.execute(
                "SELECT seq, ok, reason FROM aik08.verify_evidence_chain(%s) ORDER BY seq",
                (self._session_id,),
            ).fetchall()
        return IntegrityReport(tuple((r["seq"], bool(r["ok"]), r["reason"]) for r in rows))
