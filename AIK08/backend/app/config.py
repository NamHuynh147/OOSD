"""Cấu hình ứng dụng: đọc từ biến môi trường (và tệp ``.env`` nếu có, không ghi đè biến đã đặt)."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from app.core.models import (
    DEFAULT_MAX_SECONDS,
    DEFAULT_MAX_STEPS,
    DEFAULT_MAX_TOKENS,
    Limits,
)

# Ba vai trò CSDL, ba chuỗi kết nối — xem db/migrations/003_privileges.sql.
DEFAULT_OWNER_DSN = "postgresql://aik08:aik08@localhost:5432/aik08"
DEFAULT_READER_DSN = "postgresql://aik08_reader:aik08_reader_dev@localhost:5432/aik08"
DEFAULT_APP_DSN = "postgresql://aik08_app:aik08_app_dev@localhost:5432/aik08"


def load_env_file(path: Path) -> None:
    """Nạp KEY=VALUE từ tệp .env vào os.environ (bỏ qua dòng trống/chú thích; không ghi đè)."""
    if not path.is_file():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key.strip(), value)


def _str(name: str, default: str) -> str:
    return os.environ.get(name, default).strip()


def _int(name: str, default: int) -> int:
    raw = os.environ.get(name)
    return default if raw is None or not raw.strip() else int(raw)


def _float(name: str, default: float) -> float:
    raw = os.environ.get(name)
    return default if raw is None or not raw.strip() else float(raw)


def _bool(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None or not raw.strip():
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _csv(name: str, default: str) -> tuple[str, ...]:
    return tuple(
        x.strip() for x in os.environ.get(name, default).split(",") if x.strip()
    )


@dataclass(frozen=True, slots=True)
class Settings:
    # --- CSDL (psycopg, SQL thuần) ---
    owner_dsn: str = DEFAULT_OWNER_DSN
    reader_dsn: str = DEFAULT_READER_DSN
    app_dsn: str = DEFAULT_APP_DSN
    vector_search: str = "auto"  # auto | on | off

    # --- Hạn mức mặc định của phiên ---
    limits: Limits = Limits(DEFAULT_MAX_STEPS, DEFAULT_MAX_TOKENS, DEFAULT_MAX_SECONDS)
    synthesis_reserve_tokens: int = 2_500  # chừa token cho bước tổng hợp báo cáo
    max_consecutive_violations: int = 3
    max_concurrent_sessions: int = 4
    # Phục hồi phiên mồ côi (tiến trình chết giữa chừng): xem agent/recovery.py
    recover_on_start: bool = (
        True  # khi khởi động đóng mọi phiên chưa kết thúc (giả định một tiến trình)
    )
    orphan_grace_seconds: float = (
        30.0  # phiên quá max_seconds + ngưỡng này bị coi là mồ côi
    )
    sweep_interval_seconds: float = 30.0
    min_synthesis_seconds: float = (
        15.0  # còn ít hơn thì bỏ lời gọi LLM tổng hợp, dùng báo cáo trích xuất
    )

    # --- Công cụ HTTP GET ---
    api_allowed_prefixes: tuple[str, ...] = (
        "http://127.0.0.1:8000/demo/",
        "http://localhost:8000/demo/",
    )
    public_base_url: str = "http://127.0.0.1:8000"
    http_timeout_seconds: float = 8.0
    http_max_bytes: int = 200_000
    enable_demo_api: bool = True

    # --- LLM ---
    llm_provider: str = "google"  # mock | google | openai | multi
    llm_timeout_seconds: float = 30.0
    mock_llm_delay_seconds: float = (
        0.0  # chỉ cho mock: mô phỏng độ trễ LLM để thử nút Hủy trên UI/e2e
    )

    # Gemini
    gemini_api_key: str = os.getenv("GCP_API_KEY", "")
    gemini_model: str = "gemini-2.5-flash"
    gemini_base_url: str = "https://generativelanguage.googleapis.com"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    openai_base_url: str = "https://api.openai.com/v1"

    # --- OpenTelemetry ---
    otel_exporter: str = "none"  # none | console | otlp
    otel_service_name: str = "aik08-agent"

    # --- Xác thực API ---
    # Mặc định BẬT: cần ít nhất một khóa trong API_KEYS (mỗi khóa >= 16 ký tự). Chỉ khi chạy thử cục bộ mới đặt
    # API_AUTH_DISABLED=true. /health và /demo/* (dữ liệu tĩnh, chỉ GET) không cần khóa.
    api_keys: tuple[str, ...] = ()
    api_auth_disabled: bool = False

    # --- Web ---
    cors_origins: tuple[str, ...] = ("http://localhost:5173", "http://127.0.0.1:5173")

    MIN_API_KEY_LENGTH = 16

    def validate_auth(self) -> None:
        """Từ chối khởi động khi xác thực bật mà không có khóa hợp lệ (fail-closed)."""
        if self.api_auth_disabled:
            return
        if not self.api_keys:
            raise RuntimeError(
                "Chưa cấu hình API_KEYS. Đặt ít nhất một khóa (>= 16 ký tự), hoặc API_AUTH_DISABLED=true khi chạy thử cục bộ."
            )
        if any(len(k) < self.MIN_API_KEY_LENGTH for k in self.api_keys):
            raise RuntimeError(
                f"Mỗi khóa trong API_KEYS phải dài ít nhất {self.MIN_API_KEY_LENGTH} ký tự."
            )

    @classmethod
    def from_env(cls) -> Settings:
        base = Path(__file__).resolve().parents[1]
        load_env_file(base / ".env")
        load_env_file(base.parent / ".env")
        public_base = _str("PUBLIC_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
        return cls(
            owner_dsn=_str("OWNER_DATABASE_URL", DEFAULT_OWNER_DSN),
            reader_dsn=_str("READER_DATABASE_URL", DEFAULT_READER_DSN),
            app_dsn=_str("APP_DATABASE_URL", DEFAULT_APP_DSN),
            vector_search=_str("VECTOR_SEARCH", "auto").lower(),
            limits=Limits(
                _int("MAX_STEPS", DEFAULT_MAX_STEPS),
                _int("MAX_TOKENS", DEFAULT_MAX_TOKENS),
                _int("MAX_SECONDS", DEFAULT_MAX_SECONDS),
            ),
            synthesis_reserve_tokens=_int("SYNTHESIS_RESERVE_TOKENS", 2_500),
            max_consecutive_violations=_int("MAX_CONSECUTIVE_VIOLATIONS", 3),
            max_concurrent_sessions=_int("MAX_CONCURRENT_SESSIONS", 4),
            recover_on_start=_bool("RECOVER_ON_START", True),
            orphan_grace_seconds=_float("ORPHAN_GRACE_SECONDS", 30.0),
            sweep_interval_seconds=_float("SWEEP_INTERVAL_SECONDS", 30.0),
            min_synthesis_seconds=_float("MIN_SYNTHESIS_SECONDS", 15.0),
            api_allowed_prefixes=_csv(
                "API_ALLOWED_URL_PREFIXES", f"{public_base}/demo/"
            ),
            public_base_url=public_base,
            http_timeout_seconds=_float("HTTP_TIMEOUT_SECONDS", 8.0),
            http_max_bytes=_int("HTTP_MAX_BYTES", 200_000),
            enable_demo_api=_bool("ENABLE_DEMO_API", True),
            llm_provider=_str("LLM_PROVIDER", "mock").lower(),
            llm_timeout_seconds=_float("LLM_TIMEOUT_SECONDS", 30.0),
            mock_llm_delay_seconds=_float("MOCK_LLM_DELAY_SECONDS", 0.0),
            gemini_api_key=_str("GEMINI_API_KEY", ""),
            gemini_model=_str("GEMINI_MODEL", "gemini-2.5-flash"),
            gemini_base_url=_str(
                "GEMINI_BASE_URL",
                "https://generativelanguage.googleapis.com",
            ).rstrip("/"),
            openai_api_key=_str("OPENAI_API_KEY", ""),
            openai_model=_str("OPENAI_MODEL", "gpt-4o-mini"),
            openai_base_url=_str("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip(
                "/"
            ),
            otel_exporter=_str("OTEL_EXPORTER", "none").lower(),
            otel_service_name=_str("OTEL_SERVICE_NAME", "aik08-agent"),
            api_keys=_csv("API_KEYS", ""),
            api_auth_disabled=_bool("API_AUTH_DISABLED", False),
            cors_origins=_csv(
                "CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173"
            ),
        )
