from dataclasses import dataclass

from app.llm.provider import LLMProvider


@dataclass
class PlanStep:
    position: int
    goal: str
    status: str = "pending"


class Planner:
    def __init__(self, provider: LLMProvider) -> None:
        self.provider = provider

    async def plan(self, question: str) -> list[PlanStep]:
        goals = await self.provider.plan(question)
        if not 3 <= len(goals) <= 6:
            raise ValueError("The planner must return between 3 and 6 steps.")
        if any(not goal.strip() for goal in goals):
            raise ValueError("Plan steps must not be empty.")
        return [PlanStep(position=index, goal=goal.strip()) for index, goal in enumerate(goals, 1)]
