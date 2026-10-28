from abc import ABC, abstractmethod
from typing import Any

from app.evidence.models import Evidence


class ReadOnlyTool(ABC):
    name: str

    @abstractmethod
    async def execute(self, arguments: dict[str, Any]) -> tuple[Evidence, ...]:
        """Fetch evidence without changing external state."""
