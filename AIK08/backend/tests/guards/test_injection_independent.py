"""Đo InjectionGuard trên bộ mẫu độc lập (xem tests/guards/injection_independent.py).

Lô A và B đã được dùng để sửa luật nên là tập phát triển: kiểm hồi quy (không được tụt). Lô C là held-out đo MỘT lần
trước khi sửa tiếp; con số của nó (khoảng 16%) mới là ước lượng thực tế về khả năng tổng quát hóa, và được giữ làm
mốc cảnh báo: luật hiện chỉ là tín hiệu phụ, phòng thủ chính nằm ở chính sách công cụ/allowlist/ngân sách."""

import pytest

from app.guards.injection_guard import InjectionGuard
from tests.guards import injection_independent as m

GUARD = InjectionGuard()


def _rates(attacks, benign):
    missed = [t for t in attacks if not GUARD.scan(t).flagged]
    false_pos = [t for t in benign if GUARD.scan(t).flagged]
    return 1 - len(missed) / len(attacks), len(false_pos) / len(benign), missed, false_pos


@pytest.mark.parametrize("name", ["A", "B"])
def test_development_batches_do_not_regress(name):
    recall, fp, missed, false_pos = _rates(getattr(m, f"{name}_ATTACKS"), getattr(m, f"{name}_BENIGN"))
    print(f"\nlô {name} (tập phát triển): bắt {recall:.0%}, báo nhầm {fp:.0%}")
    assert recall >= 0.95, f"bỏ lọt: {missed}"
    assert fp <= 0.03, f"báo nhầm: {false_pos}"


def test_held_out_batch_c_is_reported_honestly_and_has_no_false_positives():
    recall, fp, _, false_pos = _rates(m.C_ATTACKS, m.C_BENIGN)
    print(f"\nlô C (held-out, đo lần đầu): bắt {recall:.0%}, báo nhầm {fp:.0%}")
    assert not false_pos, f"báo nhầm: {false_pos}"
    assert recall >= 0.10  # chỉ để chắc luật vẫn hoạt động; KHÔNG phải mục tiêu chất lượng


def test_quoting_examples_are_flagged_on_purpose():
    # Không phân biệt được tài liệu giáo dục trích câu tấn công với tấn công thật nên chọn thận trọng: gắn cờ.
    assert all(GUARD.scan(t).flagged for t in m.QUOTING_EXAMPLES)
