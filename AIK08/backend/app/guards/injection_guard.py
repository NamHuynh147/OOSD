"""Bộ quét prompt injection theo luật cho nội dung không đáng tin (tài liệu, phản hồi API, tiêu đề, URL).

Đây là TÍN HIỆU, không phải bằng chứng an toàn: kết quả được gắn vào bằng chứng, nội dung bị gắn cờ không
bao giờ được đưa vào prompt/báo cáo trích xuất, và orchestrator không bao giờ coi nó là chỉ thị.

Chống né tránh: trước khi so khớp, văn bản được chuẩn hóa — NFKC (chữ toàn góc, ký tự tương thích), bỏ ký tự
định dạng vô hình (zero-width, bidi, tag), đổi ký tự Cyrillic/Hy Lạp giống chữ Latin, bỏ dấu tiếng Việt, hạ
chữ thường, ghép chữ bị tách bằng khoảng trắng ("i g n o r e"). Luật viết trên dạng đã chuẩn hóa, nên cùng một
luật bắt được cả bản có dấu lẫn không dấu. ``ScanResult.text`` luôn là văn bản GỐC; ``excerpt`` lấy từ bản
đã chuẩn hóa.
"""

from __future__ import annotations

import base64
import binascii
import re
import unicodedata
from dataclasses import dataclass

from app.core.text import fold
from app.evidence.models import Finding


@dataclass(frozen=True, slots=True)
class ScanResult:
    text: str
    flagged: bool
    findings: tuple[Finding, ...]


@dataclass(frozen=True, slots=True)
class _Rule:
    rule_id: str
    category: str
    severity: str
    pattern: re.Pattern[str]
    raw: bool = False  # True: chạy trên bản không đổi chữ giống Latin (luật đa ngôn ngữ)


# Ký tự Cyrillic / Hy Lạp thường bị dùng để giả chữ Latin (đã ở dạng chữ thường sau NFKC + lower()).
_HOMOGLYPHS = str.maketrans(
    {
        "а": "a",
        "в": "b",
        "с": "c",
        "е": "e",
        "н": "h",
        "к": "k",
        "м": "m",
        "о": "o",
        "р": "p",
        "т": "t",
        "х": "x",
        "у": "y",
        "і": "i",
        "ј": "j",
        "ѕ": "s",
        "ԁ": "d",
        "ԛ": "q",
        "ԝ": "w",
        "ӏ": "l",
        "ё": "e",
        "α": "a",
        "β": "b",
        "ε": "e",
        "ι": "i",
        "κ": "k",
        "ν": "v",
        "ο": "o",
        "ρ": "p",
        "τ": "t",
        "υ": "u",
        "χ": "x",
        "ϲ": "c",
    }
)
# Chữ bị tách bằng một ký tự phân cách: "i g n o r e", "i-g-n-o-r-e", "i.g.n.o.r.e", "i_g_n_o_r_e".
_SPACED_LETTERS = re.compile(r"(?<![^\W\d_])(?:[^\W\d_][ \-._*]){3,}[^\W\d_](?![^\W\d_])")
_SEPARATORS = re.compile(r"[ \-._*]")
_LEET = str.maketrans({"0": "o", "1": "i", "3": "e", "4": "a", "5": "s", "7": "t", "@": "a", "$": "s", "!": "i"})
_BASE64_RUN = re.compile(r"(?<![A-Za-z0-9+/=])[A-Za-z0-9+/]{24,}={0,2}(?![A-Za-z0-9+/=])")
_BLANKS = re.compile(r"[ \t ]+")


def normalize(text: str) -> str:
    """Dạng chuẩn hóa để so khớp luật (xem docstring module)."""
    text = unicodedata.normalize("NFKC", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Cf" and (ch in "\n\t" or ord(ch) >= 32))
    text = text.lower().translate(_HOMOGLYPHS)
    text = fold(text)
    text = _SPACED_LETTERS.sub(lambda m: _SEPARATORS.sub("", m.group(0)), text)
    return _BLANKS.sub(" ", text)


def normalize_raw(text: str) -> str:
    """Như :func:`normalize` nhưng KHÔNG đổi chữ Cyrillic/Hy Lạp thành Latin: dùng cho luật đa ngôn ngữ."""
    text = unicodedata.normalize("NFKC", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Cf" and (ch in "\n\t" or ord(ch) >= 32))
    return _BLANKS.sub(" ", fold(text))


def _leet(norm: str) -> str:
    """Bản "giải leetspeak" (1gn0re -> ignore): chỉ đổi ký tự trong từ có lẫn chữ cái, để giữ nguyên số liệu thuần."""

    def fix(match: re.Match[str]) -> str:
        word = match.group(0)
        has_letter = any(c.isalpha() for c in word)
        return word.translate(_LEET) if has_letter else word

    return re.sub(r"[\w@$!]+", fix, norm)


def _decoded_base64(text: str, *, limit: int = 4) -> list[str]:
    """Giải mã các đoạn trông như base64 và trả về phần in được; kẻ tấn công hay giấu lệnh ở đây."""
    out: list[str] = []
    for match in _BASE64_RUN.finditer(text):
        raw = match.group(0)
        try:
            data = base64.b64decode(raw + "=" * (-len(raw) % 4), validate=True)
        except (binascii.Error, ValueError):
            continue
        decoded = data.decode("utf-8", errors="ignore")
        printable = sum(ch.isprintable() or ch in "\n\t" for ch in decoded)
        if len(decoded) >= 12 and printable / len(decoded) >= 0.9:
            out.append(decoded)
        if len(out) >= limit:
            break
    return out


_WORDS = r"(?:\W+\w+)"  # một "từ" bất kỳ giữa hai mốc (tối đa vài từ, để không bắt nhầm cả đoạn dài)

# Luật viết trên văn bản đã chuẩn hóa (không dấu, chữ thường). Giữ đủ chặt để các từ thông thường như
# "system", "delete", "ignore", "bo qua" đứng riêng KHÔNG bị coi là tiêm lệnh.
_RULES = (
    _Rule(
        "PI001",
        "instruction_override",
        "high",
        re.compile(
            r"\b(?:ignore|disregard|forget|override|bypass|bo qua|phot lo|quen)\b" + _WORDS + r"{0,4}?"
            r"\W+(?:previous|prior|above|earlier|preceding|all|any|every|your|system|safety|truoc|ben tren|moi|tat ca|cac)\b"
            + _WORDS
            + r"{0,3}?\W+(?:instructions?|prompts?|rules?|directions?|guidelines?|constraints?|restrictions?|"
            r"huong dan|chi thi|quy tac|rang buoc|gioi han)\b"
            # dạng đảo: "bo qua quy tac an toan truoc do", "ignore the rules above"
            r"|\b(?:ignore|disregard|forget|override|bypass|bo qua|phot lo)\b"
            + _WORDS
            + r"{0,3}?\W+(?:instructions?|prompts?|rules?|"
            r"directions?|guidelines?|huong dan|chi thi|quy tac)\b"
            + _WORDS
            + r"{0,3}?\W+(?:above|previous|prior|earlier|"
            r"safety|truoc do|truoc day|ben tren|an toan)\b",
            re.S,
        ),
    ),
    _Rule(
        "PI002",
        "secret_exfiltration",
        "high",
        re.compile(
            r"\b(?:reveal|print|expose|leak|dump|output|disclose|show|repeat|list|tiet lo|in ra|hien thi|cho toi xem|chep|sao chep|lap lai|liet ke)\b"
            + _WORDS
            + r"{0,5}?"
            r"\W+(?:system prompt|hidden prompt|prompt he thong|api[ _-]?keys?|secrets?|passwords?|mat khau|credentials?|"
            r"khoa api|khoa bi mat|ma truy cap|access tokens?|private keys?|hidden instructions?)\b",
            re.S,
        ),
    ),
    _Rule(
        "PI003",
        "tool_abuse",
        "high",
        re.compile(
            r"\b(?:call|invoke|execute|run|use|goi|chay|dung|thuc thi)\b"
            + _WORDS
            + r"{0,4}?\W+(?:tool|function|cong cu|ham)\b"
            + _WORDS
            + r"{0,4}?\W+(?:delete|drop|update|insert|write|remove|truncate|ghi|xoa|sua)\w*\b",
            re.S,
        ),
    ),
    _Rule(
        "PI004",
        "role_impersonation",
        "medium",
        re.compile(r"(?:^|\n)\s*(?:system|developer|assistant|admin|root)\s*:\s*\S.{1,160}"),
    ),
    _Rule(
        "PI005",
        "tool_directive",
        "medium",
        re.compile(
            r"\b(?:delete_all_\w+|drop[ _]table|rm\s+-rf|curl\s+[^\n]*\|\s*(?:sh|bash)|wget\s+[^\n]*\|\s*(?:sh|bash))"
        ),
    ),
    _Rule(
        "PI006",
        "prompt_boundary",
        "medium",
        re.compile(
            r"(?:<\|im_(?:start|end)\|>|\[/?(?:system|inst)\]|</?system>|<<\s*sys\s*>>|###\s*(?:system|instruction)\b)"
        ),
    ),
    _Rule(
        "PI007",
        "role_change",
        "high",
        re.compile(
            r"\b(?:you are now|from now on,? you|you must now|pretend (?:to be|you are)|act as (?:an? )?(?:unrestricted|jailbroken|root|admin(?:istrator)?|system)|"
            r"tu bay gio ban|ban bay gio la|hay dong vai (?:mot )?(?:he thong|quan tri|admin))\b"
            r"|\b(?:maintenance|developer|debug|dan|god) mode\b"
            + _WORDS
            + r"{0,6}?\W+(?:enabled|activated|on|full privileges|bat|kich hoat)\b"
            r"|\bfull privileges\b|\bdac quyen toi da\b"
        ),
    ),
    _Rule(
        "PI008",
        "data_exfiltration",
        "high",
        re.compile(
            r"\b(?:send|post|upload|forward|email|exfiltrate|gui|chuyen|tai len)\b" + _WORDS + r"{0,8}?"
            r"\W+(?:to|toi|den|vao)\b" + _WORDS + r"{0,3}?\W+https?://",
            re.S,
        ),
    ),
    _Rule(
        "PI009",
        "concealment",
        "high",
        re.compile(
            r"\b(?:do not|don't|never|without|dung|cho|khong duoc|khong)\b(?!\W+(?:forget|fail|hesitate|neglect|quen)\b)"
            + _WORDS
            + r"{0,3}?\W+(?:tell|inform|notify|warn|alert|"
            r"noi|bao|thong bao|canh bao)\b" + _WORDS + r"{0,3}?\W+(?:the )?(?:user|human|operator|nguoi dung)\b",
            re.S,
        ),
    ),
    _Rule(
        "PI010",
        "instruction_injection",
        "medium",
        re.compile(
            r"\b(?:new|updated|revised|real|actual|huong dan moi|chi thi moi)\s+(?:instructions?|system prompt|directives?|huong dan|chi thi)\s*:"
            r"|\bhuong dan moi\s*:|\bchi thi moi\s*:"
        ),
    ),
    _Rule(
        "PI011",
        "ai_addressing",
        "medium",
        re.compile(
            r"\b(?:attention|note to|dear|message for|gui|danh cho|luu y cho|chu y cho)\s+(?:ai|llm|assistant|language model|chatbot|agent|tro ly)\b"
            r"|\b(?:ai|llm|assistant|agent|tro ly)\s*[,:]\s*(?:you must|you should|hay|phai|bat buoc)\b"
        ),
    ),
    # ---- Lô luật bổ sung sau khi đo bằng bộ mẫu độc lập (tests/guards/injection_independent.py) ----
    _Rule(
        "PI012",
        "instruction_override",
        "high",
        # "bỏ qua/quên/phớt lờ ... luật/hướng dẫn/giới hạn" không cần chữ "trước đó"; phủ định ("đừng bỏ qua", "do not skip") thì bỏ.
        re.compile(
            r"(?<!not )(?<!don't )(?<!never )(?<!khong duoc )(?<!khong )(?<!dung )(?<!cannot )(?<!should not )"
            r"\b(?:ignore|disregard|forget|bypass|skip|circumvent|override|bo qua|phot lo|quen)\b" + _WORDS + r"{0,2}?"
            r"\W+(?:rules|instructions|guidelines|restrictions|limits|constraints|safeguards|allowlist|allow list|budget|"
            r"quy tac|huong dan|gioi han|rang buoc|ngan sach|danh sach cho phep|chinh sach)\b"
            r"|(?<!not )(?<!don't )(?<!never )(?<!khong )(?<!dung )\b(?:ignore|disregard|forget|bo qua)\b"
            + _WORDS
            + r"{0,3}?"
            r"\W+(?:above|preceding|so far|ben tren|o tren)\b"
            r"|\bno longer (?:bound|restricted|limited|required)\b"
            r"|\b(?:update|change|revision)s? (?:to|of) your (?:guidelines|rules|instructions|policy|policies|prompt)\b",
            re.S,
        ),
    ),
    _Rule(
        "PI013",
        "policy_disable",
        "high",
        re.compile(
            r"\b(?:disable|turn off|switch off|remove|lift|lifted|suspend|unlock|drop|tat|vo hieu hoa|go bo|mo khoa)\b"
            + _WORDS
            + r"{0,3}?\W+(?:the )?(?:safety|security|guardrails?|allowlist|allow list|filters?|content polic\w+|policies|"
            r"restrictions|read[- ]only|step budget|token budget|all tools|an toan|bo loc|gioi han|rang buoc|"
            r"danh sach cho phep|ngan sach)\b"
            r"|\b(?:safety|security)\s+(?:checks?|filters?|policies|rules|controls)\s+(?:should be|must be|are|is|will be|can be)\s+"
            r"(?:disabled|turned off|removed|suspended|lifted|skipped)\b"
            r"|\b(?:policies|restrictions|rules|limits) (?:were|have been|are|is) (?:lifted|removed|suspended|disabled)\b"
            r"|\b(?:admin|root|sudo|system|developer) (?:override|mode)\b(?!\w)"
            r"|\bred[- ]team(?:ing)? test\b" + _WORDS + r"{0,8}?\W+(?:disabled|skip\w*|bypass\w*|turned off)\b",
            re.S,
        ),
    ),
    _Rule(
        "PI014",
        "authority_claim",
        "medium",
        re.compile(
            r"\b(?:ceo|cto|ciso|admin\w*|manager|director|developer|owner|security team|ban giam doc|quan tri vien|"
            r"giam doc)\b"
            + _WORDS
            + r"{0,4}?\W+(?:approved|authori[sz]ed|allowed|permitted|granted|instructed|ordered|"
            r"da duyet|cho phep|chap thuan|ra lenh)\b"
            + _WORDS
            + r"{0,6}?\W+(?:you|the assistant|this assistant|the ai|"
            r"this agent|the agent|ban|tro ly)\b",
            re.S,
        ),
    ),
    _Rule(
        "PI015",
        "tool_abuse",
        "high",
        re.compile(
            r"\b(?:call|invoke|execute|run|use|goi|chay|dung|thuc thi|truy cap|gui yeu cau)\b" + _WORDS + r"{0,4}?"
            r"\W+(?:http_get_api|search_documents|read_document|write_file|delete_\w+|\w+_all_\w+|shell|bash|terminal|"
            r"cong cu\s+\w+_\w+)\b"
            r"|\{\s*\"(?:tool|function|action|name)\"\s*:\s*\"\w*(?:delete|drop|write|remove|update|exec|shell|rm)\w*\""
            r"|https?://(?:169\.254\.169\.254|metadata\.google\.internal|100\.100\.100\.200)"
            r"|\b(?:cat|type|less|more)\s+(?:/etc/(?:passwd|shadow)|~?/?\.ssh/|[^\s]*id_rsa|[^\s]*\.aws/credentials)",
            re.S,
        ),
    ),
    _Rule(
        "PI016",
        "result_dump",
        "medium",
        re.compile(
            r"\b(?:paste|copy|dump|include|print|chep|dan|in)\b"
            + _WORDS
            + r"{0,3}?\W+(?:every|all|each|toan bo|moi)\W+"
            r"(?:\w+\W+){0,2}(?:results?|matches|hits|ket qua|evidence|documents?|tai lieu)\b"
            r"|\b(?:contents? of|noi dung(?: cua)?)\W+(?:\w+\W+){0,2}(?:\.env|env file|tep \.env|credentials|api keys?|"
            r"secrets?|passwords?|mat khau)\b"
            r"|\b(?:append|include|add|paste|copy|embed|chep|them)\b"
            + _WORDS
            + r"{0,8}?\W+(?:your|the|cua ban|toan bo)\W+"
            r"(?:(?:full|whole|entire|exact)\W+)?(?:text of\W+)?(?:(?:system|hidden|internal)\W+)?"
            r"(?:instructions|prompts?|configuration|api keys?|credentials|secrets|chi thi|prompt he thong)\b",
            re.S,
        ),
    ),
    _Rule(
        "PI017",
        "output_manipulation",
        "high",
        re.compile(
            r"\b(?:do not|don't|never|dung|khong duoc)\b"
            + _WORDS
            + r"{0,2}?\W+(?:mention|include|cite|nhac|de cap)\b"
            + _WORDS
            + r"{0,4}?\W+(?:this|the)\W+(?:note|paragraph|text|section|message|doan nay|ghi chu|noi dung nay)\b"
            r"|\b(?:dung|khong duoc)\s+nhac\b" + _WORDS + r"{0,3}?\W+(?:doan nay|ghi chu nay|noi dung nay)\b"
            r"|\bregardless of (?:the )?(?:evidence|sources?|facts?|what|data|documents?)\b"
            r"|\bbat ke\W+(?:\w+\W+){0,2}(?:bang chung|nguon|su that|du lieu|tai lieu)\b"
            r"|\bwhatever the (?:question|evidence|query)\b"
            r"|\b(?:respond|reply|answer|tra loi)\s+only\s+with\b"
            r"|\b(?:cite|reference|trich dan)\s+\[?e\s*\d+\]?"
            r"|\bfabricat\w+\W+(?:\w+\W+){0,2}(?:sources?|citations?|evidence|data|results|references?)\b"
            r"|\b(?:bia dat|ngu tao)\W+(?:\w+\W+){0,2}(?:nguon|bang chung|trich dan|du lieu)\b"
            r"|\b(?:if|when|whenever)\W+(?:the\W+)?(?:user|anyone|someone)\W+asks?\W+(?:\w+\W+){0,8}?(?:answer|say|tell|respond|reply)\W+(?:that|them|him|her)\b"
            r"|\b(?:khi|neu)\s+nguoi dung\s+hoi\b" + _WORDS + r"{0,8}?\W+(?:hay\W+)?tra loi\b"
            r"|\b(?:from now on|tu nay)\b"
            + _WORDS
            + r"{0,3}?\W+(?:answer|respond|reply|tra loi)\W+(?:to\W+)?(?:every|any|all|each|moi)\W+"
            r"(?:\w+\W+){0,2}(?:question|query|request|prompt|cau hoi)\b",
            re.S,
        ),
    ),
    _Rule(
        "PI018",
        "data_exfiltration",
        "high",
        re.compile(
            r"!\[[^\]]*\]\(\s*https?://[^)\s]*[?&=][^)]*\)"
            r"|\b(?:add|append|include|embed|put|attach|them|chen)\b"
            + _WORDS
            + r"{0,8}?\W+(?:link|url|image|duong dan|hinh)\W+"
            r"(?:\w+\W+){0,3}?https?://"
            r"|\b(?:delete|erase|destroy|wipe|purge|remove|xoa|huy)\W+(?:\w+\W+){0,3}(?:evidence|audit|logs?|records|bang chung|"
            r"nhat ky)\W+(?:\w+\W+){0,8}?(?:so that|to avoid|before anyone|de khong|nobody|no one|khong ai)\b"
            r"|\b(?:thuc hien ngay|ngay lap tuc|lap tuc|hay)\W+(?:\w+\W+){0,2}(?:xoa|huy|go bo)\W+(?:\w+\W+){0,3}"
            r"(?:bang chung|tai lieu|du lieu|nhat ky)\b"
            r"|\b(?:de|so that)\W+(?:khong ai|no one|nobody)\W+(?:\w+\W+){0,2}(?:kiem tra|check|audit|notice|biet|see|know)\b",
            re.S,
        ),
    ),
    _Rule(
        "PI019",
        "role_impersonation",
        "medium",
        re.compile(
            r"[(\[<{]\s*(?:assistant|system|ai|agent|tro ly)\s*[:,]\s*\S"
            r"|<!--\s*(?:assistant|system|ai|agent|note to)"
            r"|(?:^|[.!?\n])\s*(?:hey |hi |hello )?(?:assistant|ai|agent|tro ly)\s*,\s*(?:please\s+|hay\s+)?(?:you\s+)?"
            r"(?:invoke|call|use|run|ignore|forget|send|delete|reveal|print|write|goi|xoa|gui|bo qua|tiet lo)\b"
            r"|\b(?:ai|llm|assistants?|agents?|bots?|tro ly)\b(?:\W+\w+){0,3}?\W+(?:reading|processing|summari[sz]ing|parsing|"
            r"analy[sz]ing|doc|xu ly)\W+(?:this|the|nay)\b"
            r"|\bnote to (?:the )?(?:ai|assistant|agent|model)\b"
            r"|\b(?:as|if you are) an? (?:helpful|good|obedient|smart|tot)\W+(?:ai|assistant|model)\b"
            r"|\b(?:neu ban la|la mot)\s+(?:mot\s+)?(?:ai|tro ly)\s+tot\b"
            r"|\b(?:meo|goi y|luu y|ghi chu|note|tip|hint)\s+(?:cho|for|to)\s+(?:ai|assistant|agent|tro ly)\b",
            re.S,
        ),
    ),
    _Rule(
        "PI020",
        "prompt_boundary",
        "medium",
        re.compile(
            r"(?:-{2,}|={2,}|\*{2,}|#{2,})\s*(?:end|stop)\s+of\s+(?:document|context|text|data|input|file)\b"
            r"|\b(?:new|updated)\s+system\s+(?:message|instructions?|prompt)\b"
            r"|\bsystem prompt update\b"
            r"|\b(?:higher|top|highest|overriding) priority (?:than|over) (?:the )?(?:system|previous|earlier|other|all)\b"
            r"|\b(?:decode|giai ma)\b"
            + _WORDS
            + r"{0,4}?\W+(?:base64|hex|rot13)\b"
            + _WORDS
            + r"{0,6}?\W+(?:follow|execute|run|and do|lam theo|thuc hien)\b"
            r"|\b(?:translate|dich)\b"
            + _WORDS
            + r"{0,8}?\W+(?:and then|then|roi|sau do)\W+(?:\w+\W+){0,3}(?:do|execute|follow|run|lam|thuc hien)\b",
            re.S,
        ),
    ),
    _Rule(
        "PI021",
        "instruction_override",
        "high",
        re.compile(
            # Pháp, Tây Ban Nha, Đức, Nga, Trung — "bỏ qua mọi chỉ thị trước đó".
            r"\b(?:ignorez|oubliez)\b" + _WORDS + r"{0,3}?\W+(?:instructions?|consignes?|regles)\b"
            r"|\b(?:ignora|ignore|olvida)\b" + _WORDS + r"{0,3}?\W+(?:las\W+)?(?:instrucciones|reglas|ordenes)\b"
            r"|\bignoriere\b" + _WORDS + r"{0,3}?\W+(?:anweisungen|regeln|instruktionen)\b"
            r"|\bvergiss\b" + _WORDS + r"{0,3}?\W+(?:anweisungen|regeln)\b"
            r"|(?:игнорир\w+|забудьт\w+|проигнорир\w+)"
            + _WORDS
            + r"{0,3}?\W+(?:предыдущ\w+|все|любые)\W+(?:\w+\W+){0,2}"
            r"(?:инструкци\w+|правил\w+|указани\w+)"
            r"|(?:忽略|无视|忽視|无视|忘记|忘記)(?:之前|以上|上述|先前)?(?:的)?(?:所有|全部|一切)?(?:的)?(?:指令|指示|提示|规则|規則|说明)"
            r"|(?:系统提示|系統提示)",
            re.S,
        ),
        raw=True,
    ),
    # ---- Vòng 2: tổng quát hóa theo NHÓM sau khi đo lô B (lô B từ đây là tập phát triển, không còn held-out) ----
    _Rule(
        "PI022",
        "ai_directive",
        "medium",
        re.compile(
            # Văn bản nói thẳng với/ về mô hình: "the assistant must ...", "tro ly phai ...". Loại "assistant manager/professor/to the ...".
            r"\b(?:the\W+)?(?:assistant(?!\W+(?:manager|professor|director|to\b|engineer|editor|secretary|general|principal))|"
            r"ai|summari[sz]er|llm|chatbot|language model|agent|model|bot)\W+(?:\w+\W+){0,2}?"
            r"(?:must|should|shall|needs? to|has to|is now|is hereby|is authori[sz]ed|are authori[sz]ed|will now)\W+"
            r"(?:now\W+|also\W+|quietly\W+|silently\W+)?(?:ignore|disregard|skip|bypass|behave|act|read|copy|send|forward|"
            r"reveal|print|output|delete|write|call|invoke|report|answer|respond|obey|comply|stop|drop|mark|state|claim)\b"
            r"|\b(?:authori[sz]ed|permitted|allowed) to\W+(?:\w+\W+){0,4}?(?:outside|beyond)\W+(?:the\W+)?(?:allowlist|allow list|policy|scope)\b"
            r"|\boutside (?:the )?allowlist\b",
            re.S,
        ),
    ),
    _Rule(
        "PI023",
        "output_manipulation",
        "high",
        re.compile(
            r"\b(?:pretend|assume|imagine|act as if|gia vo|gia su)\b\W+(?:that\W+|rang\W+)?(?:the\W+)?"
            r"(?:evidence|sources?|documents?|data|bang chung|tai lieu|nguon|du lieu)\b"
            r"|\bno matter what\W+(?:the\W+)?(?:sources?|evidence|documents?|data|user)\b"
            r"|\b(?:answer|respond|reply|write)\W+(?:\w+\W+){0,4}?(?:incorrectly|wrongly|falsely|deliberately wrong)\b"
            r"|\bon purpose\b" + _WORDS + r"{0,2}?\W*$"
            r"|\b(?:skip|bypass|omit|khong can|bo qua)\W+(?:the\W+)?(?:verification|validation|fact[- ]?check\w*|kiem chung|doi chieu)\b"
            r"|\b(?:mark|label|flag|danh dau)\W+(?:\w+\W+){0,3}?(?:claims?|citations?|statements?|trich dan|nhan dinh)\W+(?:\w+\W+){0,3}?"
            r"(?:as )?(?:verified|valid|correct|da kiem chung|hop le|dung)\b"
            r"|\b(?:ignore|disregard|bo qua)\W+(?:the\W+)?(?:retrieval|retrieved|search|evidence|sources?|ket qua|bang chung|nguon)\b"
            r"|\b(?:ignore|disregard|bo qua)\W+(?:\w+\W+){0,2}?(?:user|nguoi dung)(?:'s)?\W+(?:question|request|query|cau hoi|yeu cau)\b"
            r"|\binstead\W+(?:reveal|print|output|show|disclose|tiet lo|in ra)\b"
            r"|\b(?:put|place|paste|insert)\W+(?:whatever|everything|anything|all)\W+(?:it|they|the tool)\W+(?:returns?|finds?|outputs?)\b",
            re.S,
        ),
    ),
    _Rule(
        "PI024",
        "secret_exfiltration",
        "high",
        re.compile(
            r"\b(?:list|enumerate|print|show|tell me|return|repeat|liet ke|cho toi biet|nhac lai)\W+(?:\w+\W+){0,6}?"
            r"(?:your|its|ban)\W+(?:\w+\W+){0,2}?(?:instructions|rules|guidelines|prompt|configuration|quy tac|huong dan|chi thi)\b"
            r"|\b(?:quy tac|huong dan|chi thi)\W+(?:\w+\W+){0,4}?(?:ban da duoc cap|duoc cap cho ban|ban duoc giao|ban da duoc giao)\b"
            r"|\bban da duoc cap\b"
            r"|\b(?:contents? of|noi dung(?: cua)?)\W+(?:\w+\W+){0,2}?(?:your|ban)\W+(?:\w+\W+){0,1}?(?:instructions|prompt|rules|configuration)\b",
            re.S,
        ),
    ),
    _Rule(
        "PI025",
        "data_exfiltration",
        "high",
        re.compile(
            r"\b(?:fetch|download|open|visit|get|truy cap|tai)\W+https?://\S+\W+(?:\w+\W+){0,4}?"
            r"(?:execute|run|follow|obey|thuc hien|lam theo)\b"
            r"|\b(?:quietly|silently|secretly|covertly|without telling\W+\w+|lang le|am tham|bi mat)\W+(?:\w+\W+){0,2}?"
            r"(?:copy|send|forward|upload|delete|erase|gui|xoa|sao chep)\b"
            r"|\b(?:gui|chuyen|tai len|send|post|upload|forward)\b"
            + _WORDS
            + r"{0,14}?\W+(?:toi|den|to)\W+(?:\w+\W+){0,3}?https?://",
            re.S,
        ),
    ),
    _Rule(
        "PI026",
        "instruction_override",
        "high",
        re.compile(
            r"\b(?:set aside|put aside|throw away|abandon|discard|drop|ignor\w*|disregard\w*|bypass\w*|skip\w*|forget(?:ting)?)\b"
            + _WORDS
            + r"{0,3}?\W+(?:whatever|any|all|the|your|those|these|previous|earlier|prior)?\W*"
            r"(?:\w+\W+){0,2}?(?:guidelines|rules|instructions|limits|restrictions|constraints|policies)\b(?!\W+(?:for|of|on)\b)"
            r"|\b(?:chi dan|huong dan|chi thi|quy tac|instructions|rules|guidelines)\W+(?:\w+\W+){0,6}?"
            r"(?:vo hieu|het hieu luc|khong con hieu luc|void|invalid|obsolete|superseded|cancelled|canceled)\b"
            r"|\b(?:unfiltered|unrestricted|uncensored|jailbroken)\W+(?:model|assistant|ai|mode|llm)\b"
            r"|\b(?:nhiem vu moi|new task|your new task|your real task|the real task|real task)\W*(?:cua ban)?\s*:",
            re.S,
        ),
    ),
    _Rule(
        "PI027",
        "ai_addressing",
        "medium",
        re.compile(
            r"\b(?:message|note|notice|memo|tin nhan|thong bao)\s+(?:from|for|to|tu|cho|danh cho)\b[^\]\n]{0,60}?"
            r"\b(?:to|for|cho|danh cho)\s+(?:the\s+)?(?:ai|llm|assistant|agent|model|mo hinh|tro ly)\b"
            r"|\b(?:luu y|chu y|ghi chu|note|tip)\s+danh cho\s+(?:mo hinh|ai|tro ly|llm|agent)\b"
            r"|\b(?:if you can read this|neu ban doc duoc)\b",
            re.S,
        ),
    ),
    _Rule(
        "PI028",
        "multilingual",
        "high",
        re.compile(
            r"\bne\s+(?:dis|dites|dire)\s+pas\b" + _WORDS + r"{0,4}?\W+(?:a|au|l)\W*(?:utilisateur|user)\b"
            r"|\bsag\w*\W+(?:dem\W+)?(?:benutzer|nutzer)\w*\W+nicht\b"
            r"|\b(?:entferne|losche|losch\w+|loesche|loesch\w+)\W+(?:\w+\W+){0,2}?(?:alle|samtliche|saemtliche)\W+(?:\w+\W+){0,1}?"
            r"(?:dokumente|daten|beweise|protokolle)\b"
            r"|\bno\s+(?:le\s+)?(?:digas|digais|cuentes)\s+al?\s+usuario\b",
            re.S,
        ),
        raw=True,
    ),
)


class InjectionGuard:
    """Quét văn bản lấy về; giữ nguyên văn bản gốc và đính kèm các phát hiện ngắn, có giới hạn."""

    def __init__(self, *, excerpt_chars: int = 180, max_findings: int = 12) -> None:
        self.excerpt_chars = max(40, excerpt_chars)
        self.max_findings = max(1, max_findings)

    def scan(self, text: str) -> ScanResult:
        if not isinstance(text, str):
            raise TypeError("InjectionGuard chỉ nhận nội dung dạng str")
        findings: list[Finding] = []
        seen: set[tuple[str, str, int]] = set()
        norm = normalize(text)
        variants: list[tuple[str, str, bool]] = [("norm", norm, False), ("raw", normalize_raw(text), True)]
        leet = _leet(norm)
        if leet != norm:
            variants.append(("leet", leet, False))
        for i, decoded in enumerate(_decoded_base64(text)):
            variants.append((f"b64{i}", normalize(decoded), False))
        for variant, body, raw_variant in variants:
            for rule in _RULES:
                # Luật `raw` chỉ chạy trên bản raw; luật thường chạy trên mọi bản còn lại.
                if rule.raw != raw_variant:
                    continue
                for match in rule.pattern.finditer(body):
                    key = (rule.rule_id, variant, match.start())
                    if key in seen:
                        continue
                    seen.add(key)
                    start = max(0, match.start() - 50)
                    end = min(len(body), max(match.end(), start + self.excerpt_chars))
                    excerpt = " ".join(body[start:end].split())
                    if len(excerpt) > self.excerpt_chars:
                        excerpt = excerpt[: self.excerpt_chars - 1] + "…"
                    findings.append(Finding(rule.rule_id, rule.category, rule.severity, excerpt))
                    if len(findings) >= self.max_findings:
                        return ScanResult(text=text, flagged=True, findings=tuple(findings))
        return ScanResult(text=text, flagged=bool(findings), findings=tuple(findings))
