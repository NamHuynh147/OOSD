import hashlib
from dataclasses import dataclass


@dataclass(frozen=True)
class Evidence:
    id: str
    source: str
    content: str
    content_hash: str
    flagged: bool = False

    @classmethod
    def create(cls, source: str, content: str, flagged: bool = False) -> "Evidence":
        digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
        return cls(id=f"E{digest[:12]}", source=source, content=content, content_hash=digest, flagged=flagged)
