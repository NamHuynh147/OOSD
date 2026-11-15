"""ToolPolicy — allowlist công cụ (một nửa của lớp bảo vệ GuardedTool).

Nguồn sự thật là bảng ``aik08.allowed_tools`` (CSDL từ chối mọi công cụ không chỉ-đọc ở
mức CHECK). Policy chỉ đọc danh sách đó một lần khi mở phiên; không có đường nào để
*thêm* công cụ vào allowlist từ phía LLM hay từ nội dung nguồn.
"""

from __future__ import annotations

from collections.abc import Iterable

from app.errors import ToolNotAllowedError


class ToolPolicy:
    __slots__ = ("_allowed",)

    def __init__(self, allowed: Iterable[str]) -> None:
        self._allowed = frozenset(allowed)

    @property
    def allowed(self) -> tuple[str, ...]:
        return tuple(sorted(self._allowed))

    def is_allowed(self, name: object) -> bool:
        return isinstance(name, str) and name in self._allowed

    def authorize(self, name: object) -> None:
        """Ném ToolNotAllowedError nếu tên không nằm trong allowlist (so khớp CHÍNH XÁC)."""
        if not self.is_allowed(name):
            shown = name if isinstance(name, str) else repr(name)
            raise ToolNotAllowedError(shown[:100])
