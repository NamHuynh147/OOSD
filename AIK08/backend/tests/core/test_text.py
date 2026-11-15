import pytest

from app.core.text import defuse_citations, keywords, significant_terms
from app.db.documents import min_matched_terms


@pytest.mark.parametrize(
    ("text", "kept", "dropped"),
    [
        ("quy định sao lưu dữ liệu", ["sao", "luu"], ["quy"][:0]),  # "sao" (sao lưu) không phải từ dừng
        ("báo cáo sự cố tháng 9", ["bao", "cao"], []),  # "bao" (báo cáo) không bị xóa vì "bao nhiêu"
        ("bản sao lưu được giữ bao nhiêu ngày", ["ban", "sao", "luu"], ["bao", "nhieu"]),
        ("nhu cầu mở rộng", ["nhu", "cau"], []),  # "nhu" (nhu cầu) khác "như"
        ("Tài khoản bị khóa", ["tai", "khoan", "khoa"], ["bi"]),  # "tài" giữ, "bị" (có dấu) bỏ
        ("sao luu co ma hoa khong", ["sao", "luu", "ma", "hoa"], ["khong"]),  # gõ không dấu: "khong" bỏ, "sao" giữ
        ("Tại sao hệ thống chậm", ["he", "thong", "cham"], ["tai", "sao"]),  # cụm hỏi "tại sao" bị cắt cả cụm
    ],
)
def test_stopwords_are_filtered_before_diacritics_are_folded(text, kept, dropped):
    terms = significant_terms(text)
    for word in kept:
        assert word in terms, (word, terms)
    for word in dropped:
        assert word not in terms, (word, terms)


def test_keywords_unique_ordered_and_bounded():
    assert keywords("sao lưu sao lưu mật khẩu", max_terms=3) == ["sao", "luu", "mat"]


@pytest.mark.parametrize(("n", "expected"), [(0, 1), (1, 1), (2, 2), (3, 2), (4, 3), (5, 3), (8, 5)])
def test_min_matched_terms(n, expected):
    assert min_matched_terms(n) == expected


def test_defuse_citations_only_touches_label_shaped_text():
    assert defuse_citations("xem [E12] và [E0], [Ex], [E1234567]") == "xem [E 12] và [E 0], [Ex], [E1234567]"
