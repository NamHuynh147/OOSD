import pytest

from app.config import Settings
from app.tools.base import ToolResult
from app.tools.registry import ToolRegistry, default_registry


class Policy:
    def __init__(self, allowed):
        self.allowed = set(allowed)

    def is_allowed(self, name):
        return name in self.allowed

    def authorize(self, name):
        if name not in self.allowed:
            raise PermissionError(name)


class Dummy:
    name, description = "dummy", "d"
    created = 0

    def __init__(self):
        type(self).created += 1

    def execute(self, arguments):
        return ToolResult("dummy", [], "ok")


def test_only_allowed_tools_are_instantiated():
    registry = ToolRegistry()
    registry.register("dummy", Dummy)
    registry.register("other", Dummy)
    Dummy.created = 0
    tools = registry.build(None, None, None, Policy({"dummy"}))
    assert set(tools) == {"dummy"} and Dummy.created == 1


def test_duplicate_registration_is_rejected_and_unregistered_allowed_names_are_ignored():
    registry = ToolRegistry()
    registry.register("dummy", Dummy)
    with pytest.raises(ValueError):
        registry.register("dummy", Dummy)
    assert registry.build(None, None, None, Policy({"dummy", "ghost"})).keys() == {"dummy"}


def test_default_registry_has_http_tool_only_when_prefixes_configured():
    base = Settings.from_env()
    import dataclasses

    off = default_registry(dataclasses.replace(base, api_allowed_prefixes=()), documents=None)
    on = default_registry(
        dataclasses.replace(base, api_allowed_prefixes=("http://127.0.0.1:8000/demo/",)), documents=None
    )
    assert off.names == ("search_documents", "read_document")
    assert on.names == ("search_documents", "read_document", "http_get_api")
