"""Đăng ký công cụ: thêm một công cụ mới = ``registry.register(...)``, không sửa orchestrator hay API.

Công cụ chỉ được KHỞI TẠO khi allowlist của phiên (bảng ``tool_allowlist`` trong CSDL) cho phép nó, nên một
công cụ bị tắt trong CSDL không tạo client HTTP/kết nối nào. Mọi công cụ trả ra đều đã bọc ``GuardedTool``.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from app.config import Settings
from app.db.documents import DocumentRepository
from app.guards.guarded_tool import GuardedTool
from app.guards.injection_guard import InjectionGuard
from app.tools.base import ReadOnlyTool
from app.tools.document_search import DocumentSearchTool, ReadDocumentTool
from app.tools.http_get_api import HttpGetApiTool


class ToolRegistry:
    def __init__(self) -> None:
        self._factories: dict[str, Callable[[], ReadOnlyTool]] = {}

    def register(self, name: str, factory: Callable[[], ReadOnlyTool]) -> None:
        if name in self._factories:
            raise ValueError(f"Công cụ {name!r} đã được đăng ký")
        self._factories[name] = factory

    @property
    def names(self) -> tuple[str, ...]:
        return tuple(self._factories)

    def build(self, session: Any, budget: Any, evidence: Any, policy: Any) -> dict[str, GuardedTool]:
        """Chữ ký trùng ``tool_factory`` của AgentOrchestrator."""
        tools: dict[str, GuardedTool] = {}
        for name, factory in self._factories.items():
            if not policy.is_allowed(name):
                continue
            tool = factory()
            tools[name] = GuardedTool(
                tool, policy=policy, budget=budget, injection_guard=InjectionGuard(), evidence_store=evidence
            )
        return tools


def default_registry(settings: Settings, documents: DocumentRepository) -> ToolRegistry:
    registry = ToolRegistry()
    registry.register("search_documents", lambda: DocumentSearchTool(documents))
    registry.register("read_document", lambda: ReadDocumentTool(documents))
    if settings.api_allowed_prefixes:
        registry.register(
            "http_get_api",
            lambda: HttpGetApiTool(
                allowed_prefixes=settings.api_allowed_prefixes,
                timeout_seconds=settings.http_timeout_seconds,
                max_bytes=settings.http_max_bytes,
            ),
        )
    return registry
