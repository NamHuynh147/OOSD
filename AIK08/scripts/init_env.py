"""Tạo .env (mật khẩu ngẫu nhiên cho docker compose) và backend/.env từ các tệp mẫu.

    python scripts/init_env.py

Không bao giờ ghi đè tệp đã có. Chạy được trên Windows, macOS và Linux.
"""

from __future__ import annotations

import secrets
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHARED_API_KEY = secrets.token_urlsafe(32)  # cùng một khóa cho .env (compose) và backend/.env


def _fill(line: str) -> str:
    key, sep, value = line.partition("=")
    if sep and key.endswith("_PASSWORD") and not value.strip():
        return f"{key}={secrets.token_hex(16)}"
    if sep and key == "API_KEYS" and not value.strip():
        return f"{key}={SHARED_API_KEY}"
    return line


def main() -> int:
    env, example = ROOT / ".env", ROOT / ".env.example"
    if env.exists():
        print(f"Giữ nguyên {env.name} (đã có).")
    else:
        lines = [_fill(x) for x in example.read_text(encoding="utf-8").splitlines()]
        env.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"Đã tạo {env.name} với mật khẩu ngẫu nhiên.")
    backend_env = ROOT / "backend" / ".env"
    if backend_env.exists():
        print("Giữ nguyên backend/.env (đã có).")
    else:
        lines = [_fill(x) for x in (ROOT / "backend" / ".env.example").read_text(encoding="utf-8").splitlines()]
        backend_env.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print("Đã tạo backend/.env (kèm API_KEYS ngẫu nhiên); điền khóa LLM vào đó nếu dùng LLM thật.")
    print("Khóa API nằm ở dòng API_KEYS trong .env; UI sẽ hỏi khóa này ở lần mở đầu tiên.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
