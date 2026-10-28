import re

_SUSPICIOUS_PATTERNS = (
    re.compile(r"\bignore\s+(all\s+)?(previous|prior)\s+instructions\b", re.IGNORECASE),
    re.compile(r"\b(system|developer)\s+prompt\b", re.IGNORECASE),
    re.compile(r"\b(send|exfiltrate|upload)\b.{0,80}\b(data|secret|credential)s?\b", re.IGNORECASE),
    re.compile(r"\bbỏ qua\b.{0,40}\bchỉ dẫn\b", re.IGNORECASE),
)


def is_suspicious(content: str) -> bool:
    return any(pattern.search(content) for pattern in _SUSPICIOUS_PATTERNS)
