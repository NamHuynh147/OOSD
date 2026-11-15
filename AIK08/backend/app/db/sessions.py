"""SessionRepository: giao diện lưu trạng thái phiên + cài đặt PostgreSQL bằng SQL thuần (psycopg 3).

Mọi ràng buộc nghiệp vụ do CSDL cưỡng chế (xem migrations/002): máy trạng thái của phiên, ngân sách
bước/token/giây, kế hoạch 3–6 bước, bằng chứng append-only có chuỗi băm, báo cáo bắt buộc khi kết thúc
(kể cả khi bị hủy). Repository chỉ thực thi câu lệnh; ``translate_errors`` đổi lỗi ràng buộc thành
ngoại lệ miền (BudgetExceededError, InvalidStateError, ...), nên tầng trên không phụ thuộc psycopg.

Dùng pool của vai trò ``aik08_app`` — KHÔNG đụng tới nguồn tri thức (documents).
"""

from __future__ import annotations

import json
import re
from collections.abc import Sequence
from typing import Any, Protocol
from uuid import UUID

from psycopg.types.json import Jsonb

from app.core.models import (
    Action,
    Limits,
    LLMCallRecord,
    PlanItem,
    PlanStepStatus,
    Report,
    ReportDraft,
    ReportStatus,
    SessionRecord,
    SessionStatus,
    StepDecision,
    StepRecord,
    StopReason,
    Usage,
)
from app.core.text import truncate
from app.db.errors import translate_errors
from app.db.pool import Database
from app.evidence.store import EvidenceStore, PostgresEvidenceStore

# PHẢI khớp biểu thức trong trg_reports_before_insert / trg_reports_consistent (002).
CITATION_RE = re.compile(r"\[E([0-9]{1,6})\]")
MAX_ARGUMENTS_CHARS = 8_000
MAX_REQUESTED_TOOL_CHARS = 100  # khớp ck_steps_requested_tool


def cited_seqs(markdown: str) -> tuple[int, ...]:
    """Các số E# xuất hiện trong văn bản báo cáo (không trùng, tăng dần)."""
    return tuple(sorted({int(n) for n in CITATION_RE.findall(markdown)}))


class SessionRepository(Protocol):
    def create(self, query: str, limits: Limits) -> SessionRecord: ...
    def get(self, session_id: UUID) -> SessionRecord | None: ...
    def list_recent(self, limit: int = 30) -> list[SessionRecord]: ...
    def mark_running(self, session_id: UUID) -> bool: ...
    def request_cancel(self, session_id: UUID) -> SessionRecord | None: ...
    def is_cancel_requested(self, session_id: UUID) -> bool: ...
    def save_plan(self, session_id: UUID, items: Sequence[PlanItem]) -> None: ...
    def get_plan(self, session_id: UUID) -> list[PlanItem]: ...
    def set_plan_status(self, session_id: UUID, idx: int, status: PlanStepStatus) -> None: ...
    def add_step(
        self,
        session_id: UUID,
        action: Action,
        *,
        decision: StepDecision = StepDecision.RUNNING,
        tool_name: str | None = None,
        detail: str = "",
    ) -> StepRecord: ...
    def end_step(self, session_id: UUID, step_no: int, decision: StepDecision, detail: str = "") -> StepRecord: ...
    def list_steps(self, session_id: UUID) -> list[StepRecord]: ...
    def record_llm_call(self, session_id: UUID, call: LLMCallRecord) -> None: ...
    def finalize(self, session_id: UUID, stop_reason: StopReason, draft: ReportDraft) -> Report: ...
    def get_report(self, session_id: UUID) -> Report | None: ...
    def load_allowlist(self) -> tuple[str, ...]: ...
    def evidence_store(self, session_id: UUID) -> EvidenceStore: ...
    def list_unfinished(self) -> list[SessionRecord]: ...


_SESSION_SQL = """
SELECT id, query, status, stop_reason, max_steps, max_tokens, max_seconds, steps_used, tokens_used,
       cancel_requested_at, created_at, started_at, finished_at,
       COALESCE(EXTRACT(EPOCH FROM (COALESCE(finished_at, clock_timestamp()) - started_at)), 0)::float8
           AS elapsed_seconds
  FROM aik08.agent_sessions
"""

_STEP_SQL = """
SELECT session_id, step_no, requested_tool, tool_name, arguments, rationale, plan_idx, decision, detail,
       started_at, finished_at, duration_ms
  FROM aik08.steps
"""


def row_to_session(row: dict[str, Any]) -> SessionRecord:
    return SessionRecord(
        id=row["id"],
        query=row["query"],
        status=SessionStatus(row["status"]),
        stop_reason=StopReason(row["stop_reason"]) if row["stop_reason"] else None,
        limits=Limits(row["max_steps"], row["max_tokens"], row["max_seconds"]),
        usage=Usage(row["steps_used"], row["tokens_used"], float(row["elapsed_seconds"])),
        created_at=row["created_at"],
        started_at=row["started_at"],
        finished_at=row["finished_at"],
        cancel_requested_at=row["cancel_requested_at"],
    )


def row_to_step(row: dict[str, Any]) -> StepRecord:
    return StepRecord(
        session_id=row["session_id"],
        step_no=row["step_no"],
        requested_tool=row["requested_tool"],
        tool_name=row["tool_name"],
        arguments=row["arguments"],
        rationale=row["rationale"],
        plan_idx=row["plan_idx"],
        decision=StepDecision(row["decision"]),
        detail=row["detail"],
        started_at=row["started_at"],
        finished_at=row["finished_at"],
        duration_ms=row["duration_ms"],
    )


def bounded_arguments(arguments: Any) -> dict[str, Any]:
    """Bảo đảm tham số là object JSON và không phình quá cỡ (jsonb chấp nhận, nhưng ta không muốn)."""
    args = dict(arguments) if isinstance(arguments, dict) else {"_value": str(arguments)}
    encoded = json.dumps(args, ensure_ascii=False, default=str)
    if len(encoded) <= MAX_ARGUMENTS_CHARS:
        return json.loads(encoded)
    return {"_truncated": True, "preview": encoded[:500]}


class PostgresSessionRepository:
    def __init__(self, db: Database) -> None:
        self._db = db

    # ---- vòng đời phiên ------------------------------------------------------------------
    def create(self, query: str, limits: Limits) -> SessionRecord:
        with translate_errors(), self._db.app() as conn:
            row = conn.execute(
                "INSERT INTO aik08.agent_sessions (query, max_steps, max_tokens, max_seconds) "
                "VALUES (%s, %s, %s, %s) RETURNING id",
                (query, limits.max_steps, limits.max_tokens, limits.max_seconds),
            ).fetchone()
        assert row is not None
        created = self.get(row["id"])
        assert created is not None
        return created

    def get(self, session_id: UUID) -> SessionRecord | None:
        with translate_errors(), self._db.app() as conn:
            row = conn.execute(_SESSION_SQL + " WHERE id = %s", (session_id,)).fetchone()
        return row_to_session(row) if row else None

    def list_recent(self, limit: int = 30) -> list[SessionRecord]:
        with translate_errors(), self._db.app() as conn:
            rows = conn.execute(_SESSION_SQL + " ORDER BY created_at DESC LIMIT %s", (limit,)).fetchall()
        return [row_to_session(r) for r in rows]

    def list_unfinished(self) -> list[SessionRecord]:
        with translate_errors(), self._db.app() as conn:
            rows = conn.execute(
                _SESSION_SQL + " WHERE status IN ('pending', 'running', 'cancelling') ORDER BY created_at"
            ).fetchall()
        return [row_to_session(r) for r in rows]

    def mark_running(self, session_id: UUID) -> bool:
        with translate_errors(), self._db.app() as conn:
            row = conn.execute(
                "UPDATE aik08.agent_sessions SET status = 'running' WHERE id = %s AND status = 'pending' RETURNING id",
                (session_id,),
            ).fetchone()
        return row is not None

    def request_cancel(self, session_id: UUID) -> SessionRecord | None:
        """pending/running -> cancelling. Từ lúc này CSDL từ chối mọi bước mới (steps chỉ nhận khi 'running')
        nên việc hủy có hiệu lực ngay cả khi vòng lặp chưa kịp kiểm tra cờ.

        Máy trạng thái chỉ cho pending -> running nên phiên chưa bắt đầu đi qua 'running' trong cùng giao
        dịch; tác vụ nền sau đó thấy 'cancelling' và kết thúc bằng báo cáo rỗng thay vì chạy tiếp.
        Phiên đã kết thúc hoặc đang hủy thì không đổi gì (gọi lặp lại vô hại)."""
        with translate_errors(), self._db.app() as conn, conn.transaction():
            conn.execute(
                "UPDATE aik08.agent_sessions SET status = 'running' WHERE id = %s AND status = 'pending'",
                (session_id,),
            )
            conn.execute(
                "UPDATE aik08.agent_sessions SET status = 'cancelling' WHERE id = %s AND status = 'running'",
                (session_id,),
            )
        return self.get(session_id)

    def is_cancel_requested(self, session_id: UUID) -> bool:
        with translate_errors(), self._db.app() as conn:
            row = conn.execute(
                "SELECT cancel_requested_at IS NOT NULL AS requested FROM aik08.agent_sessions WHERE id = %s",
                (session_id,),
            ).fetchone()
        return bool(row and row["requested"])

    # ---- kế hoạch -------------------------------------------------------------------------
    def save_plan(self, session_id: UUID, items: Sequence[PlanItem]) -> None:
        """Chèn cả kế hoạch bằng MỘT câu INSERT (trigger mức câu lệnh kiểm tra 3–6 bước liên tục)."""
        values = ", ".join(["(%s, %s, %s, %s, %s)"] * len(items))
        params: list[Any] = []
        for it in items:
            params += [session_id, it.idx, truncate(it.title, 300), truncate(it.goal, 600), it.tool_hint]
        with translate_errors(), self._db.app() as conn:
            conn.execute(
                "INSERT INTO aik08.plan_steps (session_id, idx, title, goal, tool_hint) VALUES " + values,
                params,
            )

    def get_plan(self, session_id: UUID) -> list[PlanItem]:
        with translate_errors(), self._db.app() as conn:
            rows = conn.execute(
                "SELECT idx, title, goal, tool_hint, status FROM aik08.plan_steps WHERE session_id = %s ORDER BY idx",
                (session_id,),
            ).fetchall()
        return [PlanItem(r["idx"], r["title"], r["goal"], r["tool_hint"], PlanStepStatus(r["status"])) for r in rows]

    def set_plan_status(self, session_id: UUID, idx: int, status: PlanStepStatus) -> None:
        with translate_errors(), self._db.app() as conn:
            conn.execute(
                "UPDATE aik08.plan_steps SET status = %s WHERE session_id = %s AND idx = %s AND status = 'pending'",
                (status.value, session_id, idx),
            )

    # ---- nhật ký bước ---------------------------------------------------------------------
    def add_step(
        self,
        session_id: UUID,
        action: Action,
        *,
        decision: StepDecision = StepDecision.RUNNING,
        tool_name: str | None = None,
        detail: str = "",
    ) -> StepRecord:
        """Ghi một bước (tính vào ngân sách). CSDL cấp ``step_no`` và từ chối khi hết ngân sách."""
        requested = truncate(action.tool or "(không xác định)", MAX_REQUESTED_TOOL_CHARS)
        with translate_errors(), self._db.app() as conn:
            row = conn.execute(
                "INSERT INTO aik08.steps (session_id, requested_tool, tool_name, arguments, rationale, "
                "plan_idx, decision, detail) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING step_no",
                (
                    session_id,
                    requested,
                    tool_name,
                    Jsonb(bounded_arguments(action.arguments)),
                    truncate(action.rationale, 1_000),
                    action.plan_idx,
                    decision.value,
                    truncate(detail, 2_000),
                ),
            ).fetchone()
            assert row is not None
            step = conn.execute(_STEP_SQL + " WHERE session_id = %s AND step_no = %s", (session_id, row["step_no"]))
            record = step.fetchone()
        assert record is not None
        return row_to_step(record)

    def end_step(self, session_id: UUID, step_no: int, decision: StepDecision, detail: str = "") -> StepRecord:
        with translate_errors(), self._db.app() as conn:
            conn.execute(
                "UPDATE aik08.steps SET decision = %s, detail = %s WHERE session_id = %s AND step_no = %s",
                (decision.value, truncate(detail, 2_000), session_id, step_no),
            )
            record = conn.execute(
                _STEP_SQL + " WHERE session_id = %s AND step_no = %s", (session_id, step_no)
            ).fetchone()
        assert record is not None
        return row_to_step(record)

    def list_steps(self, session_id: UUID) -> list[StepRecord]:
        with translate_errors(), self._db.app() as conn:
            rows = conn.execute(_STEP_SQL + " WHERE session_id = %s ORDER BY step_no", (session_id,)).fetchall()
        return [row_to_step(r) for r in rows]

    def record_llm_call(self, session_id: UUID, call: LLMCallRecord) -> None:
        with translate_errors(), self._db.app() as conn:
            conn.execute(
                "INSERT INTO aik08.llm_calls (session_id, purpose, provider, model, input_tokens, "
                "output_tokens, duration_ms) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (
                    session_id,
                    call.purpose,
                    truncate(call.provider, 50),
                    truncate(call.model, 100),
                    max(0, call.input_tokens),
                    max(0, call.output_tokens),
                    max(0, call.duration_ms),
                ),
            )

    # ---- kết thúc & báo cáo -----------------------------------------------------------------
    def finalize(self, session_id: UUID, stop_reason: StopReason, draft: ReportDraft) -> Report:
        """Ghi báo cáo + trích dẫn rồi chuyển phiên sang trạng thái kết thúc — MỘT giao dịch.

        Các ràng buộc hoãn tới COMMIT (xem 002) bảo đảm: phiên kết thúc (kể cả bị hủy) phải có báo cáo;
        báo cáo complete <=> phiên completed; stop_reason khớp; [E#] trong văn bản khớp bảng trích dẫn
        và đều trỏ tới bằng chứng có thật; số bước khớp kế hoạch.
        """
        final_status = stop_reason.final_status
        report_status = ReportStatus.COMPLETE if final_status is SessionStatus.COMPLETED else ReportStatus.PARTIAL
        with translate_errors(), self._db.app() as conn, conn.transaction():
            plan = conn.execute(
                "SELECT count(*) AS planned, count(*) FILTER (WHERE status = 'done') AS done "
                "FROM aik08.plan_steps WHERE session_id = %s",
                (session_id,),
            ).fetchone()
            assert plan is not None
            conn.execute(
                "INSERT INTO aik08.reports (session_id, status, stop_reason, generated_by, markdown, "
                "warnings, steps_completed, steps_planned) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    session_id,
                    report_status.value,
                    stop_reason.value,
                    draft.generated_by,
                    draft.markdown,
                    Jsonb(list(draft.warnings)),
                    plan["done"],
                    plan["planned"],
                ),
            )
            for seq in cited_seqs(draft.markdown):
                conn.execute("INSERT INTO aik08.report_citations (session_id, seq) VALUES (%s, %s)", (session_id, seq))
            conn.execute(
                "UPDATE aik08.agent_sessions SET status = %s, stop_reason = %s WHERE id = %s",
                (final_status.value, stop_reason.value, session_id),
            )
        saved = self.get_report(session_id)
        assert saved is not None
        return saved

    def get_report(self, session_id: UUID) -> Report | None:
        with translate_errors(), self._db.app() as conn:
            row = conn.execute(
                "SELECT r.status, r.stop_reason, r.generated_by, r.markdown, r.warnings, "
                "       r.steps_completed, r.steps_planned, r.created_at, "
                "       COALESCE((SELECT array_agg(c.seq ORDER BY c.seq) FROM aik08.report_citations c "
                "                  WHERE c.session_id = r.session_id), '{}') AS cited "
                "  FROM aik08.reports r WHERE r.session_id = %s",
                (session_id,),
            ).fetchone()
        if row is None:
            return None
        return Report(
            status=ReportStatus(row["status"]),
            stop_reason=StopReason(row["stop_reason"]),
            generated_by=row["generated_by"],
            markdown=row["markdown"],
            citations=tuple(row["cited"]),
            warnings=tuple(row["warnings"]),
            steps_completed=row["steps_completed"],
            steps_planned=row["steps_planned"],
            created_at=row["created_at"],
        )

    # ---- khác -------------------------------------------------------------------------------
    def load_allowlist(self) -> tuple[str, ...]:
        with translate_errors(), self._db.app() as conn:
            rows = conn.execute("SELECT name FROM aik08.allowed_tools ORDER BY name").fetchall()
        return tuple(r["name"] for r in rows)

    def evidence_store(self, session_id: UUID) -> EvidenceStore:
        return PostgresEvidenceStore(self._db, session_id)
