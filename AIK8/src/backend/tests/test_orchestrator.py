from typing import Any

from app.core.orchestrator import AgentOrchestrator
from app.core.session import SessionState
from app.evidence.models import Evidence
from app.guards.tool_policy import ToolPolicy
from app.tools.base import ReadOnlyTool


class FakeTool(ReadOnlyTool):
    name = "document_search"

    async def execute(self, arguments: dict[str, Any]) -> tuple[Evidence, ...]:
        return (Evidence.create("policy", "Access is reviewed quarterly."),)


class FakeProvider:
    async def plan(self, question: str) -> list[str]:
        return ["find policy", "check review period", "summarize"]

    async def propose_action(self, question: str, step: str) -> dict[str, object]:
        return {"tool": "document_search", "arguments": {"query": step}}

    async def synthesize(self, question: str, evidence: tuple[Evidence, ...]) -> str:
        return f"Access is reviewed quarterly. [{evidence[0].id}]"


async def test_orchestrator_completes_read_only_research() -> None:
    orchestrator = AgentOrchestrator(
        FakeProvider(), {"document_search": FakeTool()}, ToolPolicy({"document_search"})
    )
    session = SessionState("How often is access reviewed?", 10, 2_000, 60)
    await orchestrator.run(session)
    assert session.status == "completed"
    assert session.report is not None
    assert session.used_steps == 3
    assert len(session.evidence_items()) == 1
