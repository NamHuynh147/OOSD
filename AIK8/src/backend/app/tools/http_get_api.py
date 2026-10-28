from typing import Any
from urllib.parse import urlparse

import httpx

from app.evidence.models import Evidence
from app.tools.base import ReadOnlyTool


class HttpGetApiTool(ReadOnlyTool):
    name = "http_get_api"

    def __init__(self, allowed_hosts: set[str], timeout_seconds: float = 10) -> None:
        self.allowed_hosts = frozenset(host.lower() for host in allowed_hosts)
        self.timeout_seconds = timeout_seconds

    async def execute(self, arguments: dict[str, Any]) -> tuple[Evidence, ...]:
        url = str(arguments.get("url", ""))
        parsed = urlparse(url)
        if parsed.scheme != "https" or not parsed.hostname or parsed.hostname.lower() not in self.allowed_hosts:
            raise PermissionError("HTTP tool only accepts HTTPS URLs on configured allowlisted hosts.")
        async with httpx.AsyncClient(timeout=self.timeout_seconds, follow_redirects=False) as client:
            response = await client.get(url)
            response.raise_for_status()
        return (Evidence.create(source=url, content=response.text[:20_000]),)
