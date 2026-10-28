from typing import Literal

from pydantic import BaseModel, Field


class SessionCreate(BaseModel):
    question: str = Field(min_length=3, max_length=4_000)
    max_steps: int | None = Field(default=None, ge=1)
    max_tokens: int | None = Field(default=None, ge=1)
    max_seconds: int | None = Field(default=None, ge=1)


class StepResponse(BaseModel):
    position: int
    goal: str
    status: Literal["pending", "running", "done", "skipped"]


class EvidenceResponse(BaseModel):
    id: str
    source: str
    content: str
    flagged: bool


class SessionResponse(BaseModel):
    id: str
    question: str
    status: str
    steps: list[StepResponse]
    evidence: list[EvidenceResponse]
    report: str | None
    error: str | None
    used_steps: int
    used_tokens: int
