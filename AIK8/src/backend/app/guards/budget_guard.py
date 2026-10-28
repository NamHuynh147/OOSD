import time

from app.core.session import SessionState


class BudgetExceeded(RuntimeError):
    pass


class BudgetGuard:
    def __init__(self, session: SessionState) -> None:
        self.session = session
        self.started_at = time.monotonic()

    def check(self, estimated_tokens: int = 0) -> None:
        if self.session.used_steps >= self.session.max_steps:
            raise BudgetExceeded("Maximum step count reached.")
        if self.session.used_tokens + estimated_tokens > self.session.max_tokens:
            raise BudgetExceeded("Maximum token budget reached.")
        if time.monotonic() - self.started_at >= self.session.max_seconds:
            raise BudgetExceeded("Maximum session duration reached.")
    def record(self, tokens: int) -> None:
        self.session.used_steps += 1
        self.session.used_tokens += tokens
