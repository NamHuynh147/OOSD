"""Ánh xạ lỗi PostgreSQL (SQLSTATE) sang ngoại lệ miền.

Tầng nghiệp vụ không import psycopg: mọi vi phạm ràng buộc xuất hiện dưới dạng
``IntegrityViolation`` hoặc ``BudgetExceededError``; lỗi hạ tầng (mất kết nối...) để nguyên.
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

import psycopg

from app.errors import (
    AgentError,
    BudgetExceededError,
    CitationError,
    ConstraintViolation,
    ImmutableViolation,
    IntegrityViolation,
    InvalidStateError,
    PermissionDenied,
    PlanCardinalityError,
    ReportRequiredError,
)

# Mã SQLSTATE riêng do trigger phát ra (xem 002_integrity_triggers.sql).
_CUSTOM: dict[str, type[IntegrityViolation]] = {
    "AK002": ImmutableViolation,
    "AK003": InvalidStateError,
    "AK004": PlanCardinalityError,
    "AK005": CitationError,
    "AK006": ReportRequiredError,
}


def translate(exc: psycopg.Error) -> Exception:
    """Trả về ngoại lệ miền tương ứng; nếu không phải vi phạm ràng buộc thì trả lại chính ``exc``."""
    state = exc.sqlstate or ""
    diag = exc.diag
    message = diag.message_primary or str(exc)
    detail = diag.message_detail or ""
    constraint = diag.constraint_name or ""

    if state == "AK001":  # budget_exceeded:<steps|tokens|seconds>
        dimension = message.split(":", 1)[1] if ":" in message else "steps"
        if dimension not in ("steps", "tokens", "seconds"):
            dimension = "steps"
        return BudgetExceededError(dimension, detail, from_db=True)  # type: ignore[arg-type]
    if state in _CUSTOM:
        return _CUSTOM[state](
            message, sqlstate=state, constraint=constraint, detail=detail
        )
    if state.startswith("23"):  # 23502 NOT NULL · 23503 FK · 23505 UNIQUE · 23514 CHECK
        return ConstraintViolation(
            message, sqlstate=state, constraint=constraint, detail=detail
        )
    if state in (
        "42501",
        "25006",
    ):  # insufficient_privilege · read_only_sql_transaction
        return PermissionDenied(
            message, sqlstate=state, constraint=constraint, detail=detail
        )
    return exc


@contextmanager
def translate_errors() -> Iterator[None]:
    """``with translate_errors(): ...`` — đổi lỗi ràng buộc CSDL thành ngoại lệ miền."""
    try:
        yield
    except psycopg.Error as exc:
        translated = translate(exc)
        if translated is exc:
            raise
        assert isinstance(translated, AgentError)
        raise translated from exc
