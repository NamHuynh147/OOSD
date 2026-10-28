class ToolPolicy:
    def __init__(self, allowed_tools: set[str]) -> None:
        self.allowed_tools = frozenset(allowed_tools)

    def require_allowed(self, tool_name: str) -> None:
        if tool_name not in self.allowed_tools:
            raise PermissionError(f"Tool is not allowlisted: {tool_name}")
