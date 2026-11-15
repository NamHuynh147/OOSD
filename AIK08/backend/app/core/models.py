"""Mô hình miền: giá trị bất biến (frozen dataclass) và các enum trạng thái.

Mọi quy tắc "có thể kiểm tra" ở đây đều được CSDL lặp lại bằng CHECK/trigger
(xem db/migrations). Python kiểm tra sớm để báo lỗi; CSDL là chốt chặn cuối.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import Any
from uuid import UUID

# Hạn mức mặc định theo đề: 10 bước · 20.000 token · 60 giây.
DEFAULT_MAX_STEPS = 10
DEFAULT_MAX_TOKENS = 20_000
DEFAULT_MAX_SECONDS = 60

# Trần cứng — khớp CHECK ck_sessions_max_* trong CSDL.
STEPS_RANGE = (1, 20)
TOKENS_RANGE = (1_000, 50_000)
SECONDS_RANGE = (5, 180)

PLAN_MIN_STEPS = 3
PLAN_MAX_STEPS = 6


class SessionStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    CANCELLING = "cancelling"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    BUDGET_EXHAUSTED = "budget_exhausted"
    FAILED = "failed"

    @property
    def is_terminal(self) -> bool:
        return self in TERMINAL_STATUSES


TERMINAL_STATUSES = frozenset(
    {
        SessionStatus.COMPLETED,
        SessionStatus.CANCELLED,
        SessionStatus.BUDGET_EXHAUSTED,
        SessionStatus.FAILED,
    }
)


class StopReason(StrEnum):
    ENOUGH_EVIDENCE = "enough_evidence"
    PLAN_DONE = "plan_done"
    NO_PROGRESS = "no_progress"
    CANCELLED_BY_USER = "cancelled_by_user"
    BUDGET_STEPS = "budget_steps"
    BUDGET_TOKENS = "budget_tokens"
    BUDGET_SECONDS = "budget_seconds"
    ERROR = "error"
    POLICY_VIOLATIONS = "policy_violations"

    @property
    def final_status(self) -> SessionStatus:
        """Trạng thái phiên tương ứng (khớp ck_sessions_stop_reason)."""
        return _STOP_TO_STATUS[self]


_STOP_TO_STATUS = {
    StopReason.ENOUGH_EVIDENCE: SessionStatus.COMPLETED,
    StopReason.PLAN_DONE: SessionStatus.COMPLETED,
    StopReason.NO_PROGRESS: SessionStatus.COMPLETED,
    StopReason.CANCELLED_BY_USER: SessionStatus.CANCELLED,
    StopReason.BUDGET_STEPS: SessionStatus.BUDGET_EXHAUSTED,
    StopReason.BUDGET_TOKENS: SessionStatus.BUDGET_EXHAUSTED,
    StopReason.BUDGET_SECONDS: SessionStatus.BUDGET_EXHAUSTED,
    StopReason.ERROR: SessionStatus.FAILED,
    StopReason.POLICY_VIOLATIONS: SessionStatus.FAILED,
}


class StepDecision(StrEnum):
    RUNNING = "running"
    EXECUTED = "executed"
    TOOL_ERROR = "tool_error"
    INVALID_ARGUMENTS = "invalid_arguments"
    DUPLICATE = "duplicate"
    BLOCKED_POLICY = "blocked_policy"


class ReportStatus(StrEnum):
    COMPLETE = "complete"
    PARTIAL = "partial"


class PlanStepStatus(StrEnum):
    PENDING = "pending"
    DONE = "done"
    SKIPPED = "skipped"


@dataclass(frozen=True, slots=True)
class Limits:
    """Hạn mức một phiên."""

    max_steps: int = DEFAULT_MAX_STEPS
    max_tokens: int = DEFAULT_MAX_TOKENS
    max_seconds: int = DEFAULT_MAX_SECONDS

    def __post_init__(self) -> None:
        for name, (low, high) in (
            ("max_steps", STEPS_RANGE),
            ("max_tokens", TOKENS_RANGE),
            ("max_seconds", SECONDS_RANGE),
        ):
            value = getattr(self, name)
            if (
                not isinstance(value, int)
                or isinstance(value, bool)
                or not low <= value <= high
            ):
                raise ValueError(
                    f"{name} phải là số nguyên trong khoảng {low}–{high}, nhận {value!r}."
                )


@dataclass(frozen=True, slots=True)
class Usage:
    steps: int = 0
    tokens: int = 0
    seconds: float = 0.0


@dataclass(frozen=True, slots=True)
class PlanItem:
    idx: int
    title: str
    goal: str = ""
    tool_hint: str | None = None
    status: PlanStepStatus = PlanStepStatus.PENDING


@dataclass(frozen=True, slots=True)
class Action:
    """Hành động LLM *đề xuất* — chưa được phép chạy cho tới khi qua GuardedTool."""

    kind: str  # "tool" | "finish"
    tool: str = ""
    arguments: Mapping[str, Any] = field(default_factory=dict)
    rationale: str = ""
    plan_idx: int | None = None

    @property
    def is_finish(self) -> bool:
        return self.kind == "finish"

    def signature(self) -> str:
        """Chữ ký chuẩn hóa để phát hiện hành động lặp lại."""
        return f"{self.tool}:{json.dumps(self.arguments, sort_keys=True, ensure_ascii=False, default=str)}"


@dataclass(frozen=True, slots=True)
class StepRecord:
    """Một dòng trên dòng thời gian (bảng steps)."""

    session_id: UUID
    step_no: int
    requested_tool: str
    tool_name: str | None
    arguments: Mapping[str, Any]
    rationale: str
    plan_idx: int | None
    decision: StepDecision
    detail: str
    started_at: datetime
    finished_at: datetime | None
    duration_ms: int | None


@dataclass(frozen=True, slots=True)
class SessionRecord:
    id: UUID
    query: str
    status: SessionStatus
    stop_reason: StopReason | None
    limits: Limits
    usage: Usage
    created_at: datetime
    started_at: datetime | None
    finished_at: datetime | None
    cancel_requested_at: datetime | None


@dataclass(frozen=True, slots=True)
class LLMCallRecord:
    """Một lần gọi LLM — cơ sở tính token (bảng llm_calls)."""

    purpose: str  # plan | act | synthesize
    provider: str
    model: str
    input_tokens: int
    output_tokens: int
    duration_ms: int


@dataclass(frozen=True, slots=True)
class ReportDraft:
    """Báo cáo chờ ghi. Trạng thái complete/partial và số bước do repository/CSDL xác định."""

    markdown: str
    generated_by: str  # llm | extractive
    warnings: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class Report:
    """Báo cáo cuối (hoặc một phần). ``citations`` là các số E# thực sự được trích dẫn."""

    status: ReportStatus
    stop_reason: StopReason
    generated_by: str  # "llm" | "extractive"
    markdown: str
    citations: tuple[int, ...]
    warnings: tuple[str, ...] = ()
    steps_completed: int = 0
    steps_planned: int = 0
    created_at: datetime | None = None
