from threading import Lock

from app.evidence.models import Evidence


class EvidenceStore:
    def __init__(self) -> None:
        self._items: list[Evidence] = []
        self._ids: set[str] = set()
        self._lock = Lock()

    @property
    def items(self) -> tuple[Evidence, ...]:
        with self._lock:
            return tuple(self._items)

    def append_many(self, evidence: tuple[Evidence, ...]) -> None:
        with self._lock:
            for item in evidence:
                if item.id not in self._ids:
                    self._items.append(item)
                    self._ids.add(item.id)
