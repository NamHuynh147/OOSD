"""API demo chỉ-đọc để minh họa công cụ ``http_get_api`` mà không cần dịch vụ bên ngoài.

Mọi route là GET, trả dữ liệu tĩnh (không đọc/ghi CSDL, không nhận tham số có tác dụng phụ). Công cụ HTTP của
agent chỉ được gọi các URL nằm dưới tiền tố ``API_ALLOWED_URL_PREFIXES`` (mặc định ``<PUBLIC_BASE_URL>/demo/``).
Tắt bằng ``ENABLE_DEMO_API=false``.
"""

from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter(prefix="/demo", tags=["demo"])

SERVICES = [
    {"service": "thanh-toan", "sla_percent": 99.95, "availability_30d_percent": 99.97, "status": "ok"},
    {"service": "dang-nhap-sso", "sla_percent": 99.9, "availability_30d_percent": 99.92, "status": "ok"},
    {"service": "bao-cao", "sla_percent": 99.5, "availability_30d_percent": 99.41, "status": "degraded"},
    {"service": "thong-bao", "sla_percent": 99.5, "availability_30d_percent": 99.8, "status": "ok"},
]


@router.get("/status")
def status() -> dict[str, object]:
    """Trạng thái dịch vụ nội bộ (dữ liệu minh họa)."""
    return {
        "as_of": "2026-10-01T00:00:00Z",
        "services": SERVICES,
        "note": "Dữ liệu minh họa cho công cụ http_get_api; không phải số liệu vận hành thật.",
    }


@router.get("/sla")
def sla() -> dict[str, object]:
    return {"window_days": 30, "targets": {s["service"]: s["sla_percent"] for s in SERVICES}}


@router.get("/maintenance", response_class=PlainTextResponse)
def maintenance() -> str:
    return "Cửa sổ bảo trì cơ sở dữ liệu thanh toán: 02:00–03:30 sáng Chủ nhật hằng tuần (dữ liệu minh họa)."
