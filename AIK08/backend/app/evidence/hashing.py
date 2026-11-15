"""Công thức nối băm — PHẢI trùng với ``aik08.evidence_chain_hash()`` trong 002_integrity_triggers.sql:

    chain_hash = sha256_hex( prev | seq | step_no | source_uri | raw_sha256 | content_sha256 )

CSDL là bên tính chính thức; bản Python chỉ dùng để đối chiếu độc lập trong test (tests/evidence).
"""

from __future__ import annotations

import hashlib

ZERO_HASH = "0" * 64


def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def chain_hash(prev_hash: str, seq: int, step_no: int, source_uri: str, raw_sha256: str, content_sha256: str) -> str:
    return sha256_hex("|".join((prev_hash, str(seq), str(step_no), source_uri, raw_sha256, content_sha256)))
