"""Embedding để lưu trong pgvector.

``HashingEmbedder`` là phép nhúng "băm từ" (hashing trick) 256 chiều, hoàn toàn cục bộ và
xác định — đủ để chạy demo offline. Muốn ngữ nghĩa thật, cài một ``EmbeddingProvider`` khác
(gọi API nhúng) có cùng số chiều với cột ``documents.embedding``.
"""

from __future__ import annotations

import hashlib
import math
from typing import Protocol

from app.core.text import significant_terms

EMBEDDING_DIM = 256


class EmbeddingProvider(Protocol):
    dim: int

    def embed(self, text: str) -> list[float] | None:
        """Vector đã chuẩn hóa L2, hoặc None nếu văn bản không có đặc trưng nào."""


class HashingEmbedder:
    dim = EMBEDDING_DIM

    def embed(self, text: str) -> list[float] | None:
        tokens = significant_terms(text)
        features = [(t, 1.0) for t in tokens] + [(f"{a}_{b}", 0.5) for a, b in zip(tokens, tokens[1:], strict=False)]
        if not features:
            return None
        vec = [0.0] * self.dim
        for feature, weight in features:
            digest = hashlib.blake2b(feature.encode("utf-8"), digest_size=8).digest()
            index = int.from_bytes(digest[:4], "big") % self.dim
            sign = 1.0 if digest[4] & 1 else -1.0
            vec[index] += sign * weight
        norm = math.sqrt(sum(v * v for v in vec))
        if norm == 0.0:
            return None
        return [v / norm for v in vec]


def to_pgvector(vec: list[float]) -> str:
    """Định dạng văn bản của pgvector: ``[0.1,0.2,...]`` (dùng với tham số ``%s::vector``)."""
    return "[" + ",".join(f"{v:.6f}" for v in vec) + "]"
