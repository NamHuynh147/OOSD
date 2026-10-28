import asyncio
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Literal
from uuid import uuid4

from app.core.planner import PlanStep
from app.evidence.models import Evidence
from app.evidence.store import EvidenceStore

SessionStatus = Literal[
    "queued", "running", "completed", "budget_exhausted", "cancelled", "error"
]
StepStatus = Literal["pending", "running", "done", "skipped"]


@dataclass
class SessionState:
    question: str
    max_steps: int
    max_tokens: int
    max_seconds: int
    id: str = field(default_factory=lambda: str(uuid4()))
    status: SessionStatus = "queued"
    steps: list[PlanStep] = field(default_factory=list)
    report: str | None = None
    error: str | None = None
    used_steps: int = 0
    used_tokens: int = 0
    started_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    cancel_event: asyncio.Event = field(default_factory=asyncio.Event)
    evidence: EvidenceStore = field(default_factory=EvidenceStore)

    def request_cancel(self) -> None:
        self.cancel_event.set()

    def evidence_items(self) -> tuple[Evidence, ...]:
        return self.evidence.items
