"""Tiện ích xử lý văn bản (tiếng Việt/Anh): bỏ dấu, tách từ khóa, tách câu, ước lượng token."""

from __future__ import annotations

import math
import re
import unicodedata

_WORD = re.compile(r"[a-z0-9]+")
_BULLET = re.compile(r"^\s*(?:[-*•–]+|\d+[.)])\s+")
_SENTENCE_END = re.compile(r"(?<=[.!?;])\s+(?=[A-ZÀ-Ỹ0-9\"'(\[])")

# Từ dừng được lọc TRƯỚC khi bỏ dấu. Bỏ dấu trước sẽ làm từ nội dung va chạm với từ dừng và bị xóa nhầm:
# "sao lưu" (backup) <- "sao" (tại sao), "báo cáo" <- "bao" (bao nhiêu), "bản sao" <- "ban" (bạn),
# "đề"/"dê" <- "de" (để), "thể" <- "the" (thế), "nhu cầu" <- "nhu" (như), "tải" <- "tai" (tại).
# Nên có ba tầng: cụm từ hỏi (cắt cả cụm), từ dừng CÓ dấu (so khớp đúng dấu), và từ dừng không dấu chỉ gồm
# các từ không va chạm với từ nội dung thường gặp (dùng khi người dùng gõ không dấu).
_STOP_PHRASES = re.compile(
    r"\b(?:bao nhiêu|bao lâu|như thế nào|ra sao|là gì|tại sao|vì sao|hôm nay|hiện nay|bây giờ|cho biết|cho tôi|cho xem|"
    r"hãy cho|xin hãy|bao nhieu|bao lau|nhu the nao|la gi|tai sao|vi sao|hom nay|hien nay|bay gio|cho biet|cho toi|cho xem)\b"
)
_STOP_ACCENTED = frozenset(
    [
        "là",
        "và",
        "của",
        "cho",
        "các",
        "những",
        "một",
        "như",
        "thế",
        "nào",
        "gì",
        "có",
        "không",
        "được",
        "trong",
        "với",
        "để",
        "đã",
        "sẽ",
        "đang",
        "tại",
        "từ",
        "về",
        "hay",
        "hoặc",
        "khi",
        "nếu",
        "thì",
        "mà",
        "bị",
        "do",
        "này",
        "kia",
        "ở",
        "ra",
        "vào",
        "lên",
        "xuống",
        "hiện",
        "hành",
        "nhất",
        "cần",
        "phải",
        "nên",
        "cũng",
        "rất",
        "tôi",
        "bạn",
        "chúng",
        "mình",
        "ai",
        "đâu",
        "vì",
        "bằng",
        "qua",
        "theo",
        "trên",
        "dưới",
        "sau",
        "trước",
        "giữa",
        "việc",
        "cái",
        "hãy",
        "giúp",
        "xin",
        "tìm",
        "nhiêu",
        "lâu",
    ]
)
_STOP_ASCII = frozenset(
    [
        "la",
        "va",
        "cua",
        "cho",
        "cac",
        "nhung",
        "mot",
        "nao",
        "gi",
        "khong",
        "duoc",
        "trong",
        "voi",
        "se",
        "hay",
        "hoac",
        "khi",
        "neu",
        "thi",
        "nay",
        "kia",
        "the",
        "a",
        "an",
        "of",
        "and",
        "or",
        "to",
        "in",
        "on",
        "for",
        "is",
        "are",
        "was",
        "were",
        "be",
        "been",
        "what",
        "which",
        "how",
        "who",
        "when",
        "where",
        "why",
        "with",
        "about",
        "from",
        "by",
        "at",
        "as",
        "it",
        "this",
        "that",
        "these",
        "those",
        "do",
        "does",
        "did",
        "can",
        "could",
        "should",
        "would",
        "please",
    ]
)
_WORD = re.compile(r"\w+", re.UNICODE)


def _has_diacritics(token: str) -> bool:
    return token != fold(token)


def significant_terms(text: str) -> list[str]:
    """Từ mang nghĩa của ``text``, đã bỏ dấu + hạ chữ thường, giữ thứ tự và lặp lại (đã lọc từ dừng đúng cách)."""
    lowered = unicodedata.normalize("NFC", text).lower()
    lowered = _STOP_PHRASES.sub(" ", lowered)
    out: list[str] = []
    for token in _WORD.findall(lowered):
        if token in (_STOP_ACCENTED if _has_diacritics(token) else _STOP_ASCII):
            continue
        folded = fold(token)
        if len(folded) < 2 and not folded.isdigit():
            continue
        out.extend(_WORD.findall(folded))
    return out


def fold(text: str) -> str:
    """Bỏ dấu + hạ chữ thường: ``"Mật khẩu"`` -> ``"mat khau"`` (cùng quy tắc fold_vi trong CSDL)."""
    decomposed = unicodedata.normalize("NFD", text.replace("đ", "d").replace("Đ", "D"))
    stripped = "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")
    return unicodedata.normalize("NFC", stripped).lower()


def tokenize(text: str) -> list[str]:
    return _WORD.findall(fold(text))


def keywords(text: str, *, max_terms: int = 12) -> list[str]:
    """Từ khóa duy nhất, giữ thứ tự xuất hiện, bỏ từ dừng và từ 1 ký tự (lọc từ dừng trước khi bỏ dấu)."""
    seen: dict[str, None] = {}
    for tok in significant_terms(text):
        seen.setdefault(tok, None)
        if len(seen) >= max_terms:
            break
    return list(seen)


def split_sentences(text: str) -> list[str]:
    """Tách thành các câu/dòng ngắn (mỗi dòng của danh sách là một đơn vị)."""
    out: list[str] = []
    for line in text.splitlines():
        line = _BULLET.sub("", line).strip()
        if not line:
            continue
        for part in _SENTENCE_END.split(line):
            part = part.strip()
            if len(part) >= 3:
                out.append(part)
    return out


def score_sentence(sentence: str, terms: list[str]) -> float:
    """Tỷ lệ từ khóa truy vấn xuất hiện trong câu (0..1)."""
    if not terms:
        return 0.0
    words = set(tokenize(sentence))
    return sum(1 for t in terms if t in words) / len(terms)


def best_sentences(text: str, terms: list[str], *, limit: int = 3, min_score: float = 0.0) -> list[str]:
    """Các câu phù hợp nhất với từ khóa, trả lại theo thứ tự gốc trong văn bản."""
    sentences = split_sentences(text)
    scored = [(score_sentence(s, terms), i, s) for i, s in enumerate(sentences)]
    scored = [x for x in scored if x[0] >= min_score and (x[0] > 0 or not terms)]
    top = sorted(scored, key=lambda x: (-x[0], x[1]))[:limit]
    return [s for _, _, s in sorted(top, key=lambda x: x[1])]


def estimate_tokens(text: str) -> int:
    """Ước lượng thận trọng (~3 ký tự/token; tiếng Việt có dấu tốn token hơn tiếng Anh)."""
    return max(1, math.ceil(len(text) / 3))


# Khớp đúng biểu thức trích dẫn của CSDL (trg_reports_before_insert): chỉ chữ số ASCII.
_CITATION_LIKE = re.compile(r"\[E([0-9]{1,6})\]")


def defuse_citations(text: str) -> str:
    """Vô hiệu hóa chuỗi giống trích dẫn trong văn bản KHÔNG tin cậy: ``[E12]`` -> ``[E 12]``.

    Câu hỏi, tiêu đề, nội dung và nguồn của bằng chứng đều có thể chứa ``[E99]``. Nếu chúng được chép
    nguyên vào báo cáo, CSDL coi đó là trích dẫn tới bằng chứng không tồn tại và từ chối kết thúc phiên.
    Chỉ nhãn do hệ thống tự sinh mới được phép có dạng ``[E#]``.
    """
    return _CITATION_LIKE.sub(r"[E \1]", text)


def truncate(text: str, limit: int, ellipsis: str = "…") -> str:
    if limit <= 0:
        return ""
    if len(text) <= limit:
        return text
    return text[: max(0, limit - len(ellipsis))].rstrip() + ellipsis
