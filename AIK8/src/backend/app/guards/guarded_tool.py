import json
from typing import Any

from opentelemetry import trace

from app.core.session import SessionState
from app.evidence.models import Evidence
from app.evidence.store import EvidenceStore
from app.guards.budget_guard import BudgetGuard
from app.guards.injection_guard import is_suspicious
from app.guards.tool_policy import ToolPolicy
from app.tools.base import ReadOnlyTool

tracer = trace.get_tracer(__name__)


class GuardedTool:
    def __init__(
        self,
        tool: ReadOnlyTool,
        policy: ToolPolicy,
        budget: BudgetGuard,
        evidence_store: EvidenceStore,
    ) -> None:
        self.tool = tool
        self.policy = policy
        self.budget = budget
        self.evidence_store = evidence_store

    async def execute(self, session: SessionState, arguments: dict[str, Any]) -> tuple[Evidence, ...]:
        with tracer.start_as_current_span("guarded_tool.execute") as span:
            span.set_attribute("tool.name", self.tool.name)
            self.policy.require_allowed(self.tool.name)
            self.budget.check()
            results = await self.tool.execute(arguments)
            estimated_tokens = sum(max(1, len(item.content) // 4) for item in results)
            self.budget.check(estimated_tokens)
            marked = tuple(
                Evidence.create(
                    source=item.source,
                    content=item.content,
                    flagged=item.flagged or is_suspicious(item.content),
                )
                for item in results
            )
            self.evidence_store.append_many(marked)
            self.budget.record(estimated_tokens)
            span.set_attribute("evidence.count", len(marked))
            span.set_attribute("budget.estimated_tokens", estimated_tokens)
            return marked
