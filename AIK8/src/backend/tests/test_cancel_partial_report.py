import asyncio
from typing import Any

from app.core.orchestrator import AgentOrchestrator
from app.core.session import SessionState
from app.evidence.models import Evidence
from app.guards.tool_policy import ToolPolicy
from app.tools.base import ReadOnlyTool


class FakeTool(ReadOnlyTool):
    name = "document_search"
    session: SessionState | None = None

    async def execute(self, arguments: dict[str, Any]) -> tuple[Evidence, ...]:
        if self.session is not None:
            self.session.request_cancel()
        return (Evidence.create("test", "Relevant result"),)


class FakeProvider:
    def __init__(self) -> None:
        self.session: SessionState | None = None
        self.actions = 0

    async def plan(self, question: str) -> list[str]:
        return ["find first", "find next", "summarize"]

    async def propose_action(self, question: str, step: str) -> dict[str, object]:
        self.actions += 1
        if self.actions == 2 and self.session is not None:
            self.session.request_cancel()
        return {"tool": "document_search", "arguments": {"query": step}}

    async def synthesize(self, question: str, evidence: tuple[Evidence, ...]) -> str:
        return "Partial result [E" + evidence[0].content_hash[:12] + "]"


async def test_cancelled_session_keeps_partial_report() -> None:
    provider = FakeProvider()
    tool = FakeTool()
    orchestrator = AgentOrchestrator(
        provider, {"document_search": tool}, ToolPolicy({"document_search"})
    )
    session = SessionState("question", max_steps=10, max_tokens=2_000, max_seconds=60)
    provider.session = session
    tool.session = session
    await orchestrator.run(session)
    assert session.status == "cancelled"
    assert session.report is not None
    assert len(session.evidence_items()) == 1


def test_session_cancel_token_is_settable() -> None:
    session = SessionState("question", max_steps=10, max_tokens=100, max_seconds=60)
    session.request_cancel()
    assert session.cancel_event.is_set()
