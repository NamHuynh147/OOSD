import pytest

from app.guards.tool_policy import ToolPolicy


def test_tool_outside_allowlist_is_blocked() -> None:
    policy = ToolPolicy({"document_search"})
    with pytest.raises(PermissionError):
        policy.require_allowed("delete_document")
