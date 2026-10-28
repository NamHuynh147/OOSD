from typing import Protocol

from app.evidence.models import Evidence


class LLMProvider(Protocol):
    async def plan(self, question: str) -> list[str]: ...

    async def propose_action(self, question: str, step: str) -> dict[str, object]: ...

    async def synthesize(self, question: str, evidence: tuple[Evidence, ...]) -> str: ...
