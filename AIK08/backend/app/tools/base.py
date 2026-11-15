"""Minimal interface shared by strictly read-only tools."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True, slots=True)
class ToolResult:
    tool_name: str
    data: Any
    summary: str
    evidence_labels: tuple[str, ...] = ()
    flagged: bool = False


class ReadOnlyTool(Protocol):
    name: str
    description: str

    def validate(self, arguments: dict[str, Any]) -> object:
        """Ném InvalidToolArgumentsError nếu tham số sai (gọi trước khi ghi bước, nên có thể ghi
        quyết định ``invalid_arguments``); ``execute`` cũng gọi lại."""
        ...

    def execute(self, arguments: dict[str, Any]) -> ToolResult: ...
