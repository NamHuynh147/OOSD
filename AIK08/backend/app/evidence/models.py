"""Mô hình bằng chứng — toàn bộ là dataclass bất biến (frozen)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, slots=True)
class Finding:
    """Một dấu hiệu nghi ngờ do InjectionGuard phát hiện trong nội dung nguồn."""

    rule_id: str
    category: str
    severity: str  # high | medium | low
    excerpt: str

    def to_dict(self) -> dict[str, str]:
        return {
            "rule_id": self.rule_id,
            "category": self.category,
            "severity": self.severity,
            "excerpt": self.excerpt,
        }

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> Finding:
        return cls(data["rule_id"], data["category"], data["severity"], data.get("excerpt", ""))


@dataclass(frozen=True, slots=True)
class EvidenceDraft:
    """Bằng chứng chờ ghi: nội dung ĐÃ qua InjectionGuard, kèm băm (hex) của nội dung gốc."""

    tool_name: str
    source_uri: str
    title: str
    content: str
    raw_sha256: str
    flagged: bool = False
    findings: tuple[Finding, ...] = ()


@dataclass(frozen=True, slots=True)
class Evidence:
    """Bằng chứng đã lưu: có số thứ tự E# và vị trí trong chuỗi băm (do CSDL cấp)."""

    session_id: UUID
    seq: int
    step_no: int
    tool_name: str
    source_uri: str
    title: str
    content: str
    raw_sha256: str
    content_sha256: str
    prev_hash: str
    chain_hash: str
    flagged: bool
    findings: tuple[Finding, ...]
    retrieved_at: datetime

    @property
    def label(self) -> str:
        return f"E{self.seq}"


@dataclass(frozen=True, slots=True)
class IntegrityReport:
    """Kết quả kiểm chứng chuỗi băm: (số E#, còn nguyên vẹn?, lý do)."""

    results: tuple[tuple[int, bool, str], ...]

    @property
    def ok(self) -> bool:
        return all(ok for _, ok, _ in self.results)

    @property
    def broken(self) -> tuple[int, ...]:
        return tuple(seq for seq, ok, _ in self.results if not ok)
