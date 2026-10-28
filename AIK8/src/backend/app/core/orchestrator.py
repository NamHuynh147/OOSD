import asyncio
from collections.abc import Mapping
from typing import Any

from opentelemetry import trace

from app.core.planner import Planner
from app.core.session import SessionState
from app.core.synthesizer import ReportSynthesizer
from app.evidence.models import Evidence
from app.guards.budget_guard import BudgetExceeded, BudgetGuard
from app.guards.guarded_tool import GuardedTool
from app.guards.tool_policy import ToolPolicy
from app.llm.provider import LLMProvider
from app.tools.base import ReadOnlyTool

tracer = trace.get_tracer(__name__)


class AgentOrchestrator:
    def __init__(
        self,
        provider: LLMProvider,
        tools: Mapping[str, ReadOnlyTool],
        tool_policy: ToolPolicy,
    ) -> None:
        self.provider = provider
        self.tools = tools
        self.tool_policy = tool_policy
        self.planner = Planner(provider)
        self.synthesizer = ReportSynthesizer(provider)

    async def run(self, session: SessionState) -> None:
        session.status = "running"
        guard = BudgetGuard(session)
        try:
            session.steps = await self.planner.plan(session.question)
            for step in session.steps:
                with tracer.start_as_current_span("agent.step") as span:
                    span.set_attribute("session.id", session.id)
                    span.set_attribute("step.position", step.position)
                    span.set_attribute("step.goal", step.goal)
                    if session.cancel_event.is_set():
                        step.status = "skipped"
                        continue
                    step.status = "running"
                    action = await self.provider.propose_action(session.question, step.goal)
                    if session.cancel_event.is_set():
                        step.status = "skipped"
                        continue
                    tool = self.tools.get(action["tool"])
                    if tool is None:
                        raise PermissionError(f"Unknown tool: {action['tool']}")
                    guarded = GuardedTool(tool, self.tool_policy, guard, session.evidence)
                    try:
                        await guarded.execute(session, action.get("arguments", {}))
                    except BudgetExceeded:
                        step.status = "skipped"
                        for later in session.steps[step.position:]:
                            later.status = "skipped"
                        session.status = "budget_exhausted"
                        span.set_attribute("step.status", step.status)
                        break
                    step.status = "done"
                    span.set_attribute("step.status", step.status)
            else:
                session.status = "cancelled" if session.cancel_event.is_set() else "completed"
            session.report = await self.synthesizer.synthesize(session.question, session.evidence_items())
            if session.cancel_event.is_set() and session.status == "running":
                session.status = "cancelled"
        except asyncio.CancelledError:
            session.request_cancel()
            session.status = "cancelled"
            session.report = await self.synthesizer.synthesize(session.question, session.evidence_items())
        except Exception as exc:
            session.status = "error"
            session.error = str(exc)
            if session.evidence.items:
                session.report = await self.synthesizer.synthesize(session.question, session.evidence_items())
