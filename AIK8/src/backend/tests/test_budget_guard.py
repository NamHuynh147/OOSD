import pytest

from app.core.session import SessionState
from app.guards.budget_guard import BudgetExceeded, BudgetGuard


def test_token_budget_stops_before_it_is_exceeded() -> None:
    session = SessionState("question", max_steps=2, max_tokens=5, max_seconds=60)
    guard = BudgetGuard(session)
    with pytest.raises(BudgetExceeded, match="token"):
        guard.check(6)


def test_step_budget_stops_at_limit() -> None:
    session = SessionState("question", max_steps=1, max_tokens=10, max_seconds=60)
    session.used_steps = 1
    with pytest.raises(BudgetExceeded, match="step"):
        BudgetGuard(session).check()
