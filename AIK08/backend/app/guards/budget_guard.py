"""BudgetGuard — giới hạn bước · token · giây (một nửa của lớp bảo vệ GuardedTool).

Đây là tuyến *nhanh* trong tiến trình: tránh gọi LLM/tool vô ích khi đã hết ngân sách.
Tuyến *cuối cùng* nằm ở CSDL (trigger ``trg_steps_before_insert`` từ chối bước thứ max+1,
token vượt hạn mức, hoặc quá hạn giây), nên dù guard này sai thì dữ liệu vẫn đúng.

Mặc định theo đề: 10 bước · 20.000 token · 60 giây.
"""

from __future__ import annotations

import threading
import time
from collections.abc import Callable

from app.core.models import Limits, Usage
from app.errors import BudgetExceededError


class BudgetGuard:
    def __init__(
        self,
        limits: Limits,
        *,
        reserve_tokens: int = 2_500,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self.limits = limits
        # Chừa token cho bước tổng hợp báo cáo; ngân sách nhỏ thì chỉ chừa tối đa 1/4.
        self.reserve_tokens = max(0, min(reserve_tokens, limits.max_tokens // 4))
        self._clock = clock
        self._lock = threading.Lock()
        self._started: float | None = None
        self._steps = 0
        self._tokens = 0

    # ---- đo đạc ----------------------------------------------------------------------
    def start(self) -> None:
        with self._lock:
            if self._started is None:
                self._started = self._clock()

    @property
    def elapsed(self) -> float:
        return 0.0 if self._started is None else max(0.0, self._clock() - self._started)

    @property
    def remaining_seconds(self) -> float:
        return max(0.0, self.limits.max_seconds - self.elapsed)

    @property
    def steps_left(self) -> int:
        return max(0, self.limits.max_steps - self._steps)

    def usage(self) -> Usage:
        return Usage(self._steps, self._tokens, round(self.elapsed, 3))

    # ---- ghi nhận --------------------------------------------------------------------
    def charge_step(self) -> None:
        with self._lock:
            self._steps += 1

    def charge_tokens(self, tokens: int) -> None:
        with self._lock:
            self._tokens += max(0, int(tokens))

    # ---- kiểm tra --------------------------------------------------------------------
    def check(self, *, extra_tokens: int = 0, reserve: bool = True) -> None:
        """Ném BudgetExceededError nếu hết token hoặc thời gian.

        ``extra_tokens``: ước lượng token của lời gọi sắp thực hiện. ``reserve``: có chừa
        phần dành cho báo cáo hay không (bước tổng hợp tự nó gọi với reserve=False).
        """
        if self._started is not None and self.elapsed >= self.limits.max_seconds:
            raise BudgetExceededError("seconds", f"{self.elapsed:.1f}/{self.limits.max_seconds} giây")
        held = self.reserve_tokens if reserve else 0
        if self._tokens + extra_tokens + held > self.limits.max_tokens:
            raise BudgetExceededError(
                "tokens", f"{self._tokens}+{extra_tokens} (+{held} dự phòng)/{self.limits.max_tokens} token"
            )
        if self._steps > self.limits.max_steps:  # chỉ xảy ra nếu có lỗi đếm; CSDL cũng chặn
            raise BudgetExceededError("steps", f"{self._steps}/{self.limits.max_steps} bước")

    def ensure_step_available(self) -> None:
        if self._steps >= self.limits.max_steps:
            raise BudgetExceededError("steps", f"{self._steps}/{self.limits.max_steps} bước")

    def can_afford(self, tokens: int, *, reserve: bool = False) -> bool:
        try:
            self.check(extra_tokens=tokens, reserve=reserve)
        except BudgetExceededError:
            return False
        return True
