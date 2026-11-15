"""Xác thực bằng API key: header ``X-API-Key`` hoặc ``Authorization: Bearer <key>``.

So sánh thời gian hằng (``hmac.compare_digest``) với *mọi* khóa đã cấu hình để không lộ khóa nào khớp qua thời gian
phản hồi. Khóa không bao giờ được ghi log hay đưa vào thông báo lỗi.
"""

from __future__ import annotations

import hmac

from fastapi import HTTPException, Request


def _presented_key(request: Request) -> str:
    key = request.headers.get("x-api-key", "").strip()
    if key:
        return key
    auth = request.headers.get("authorization", "")
    scheme, _, token = auth.partition(" ")
    return token.strip() if scheme.lower() == "bearer" else ""


def key_is_valid(presented: str, valid_keys: tuple[str, ...]) -> bool:
    ok = False
    for candidate in valid_keys:
        ok |= hmac.compare_digest(presented.encode(), candidate.encode())
    return ok and bool(presented)


def require_api_key(request: Request) -> None:
    settings = request.app.state.settings
    if settings.api_auth_disabled:
        return
    if not key_is_valid(_presented_key(request), settings.api_keys):
        raise HTTPException(
            status_code=401,
            detail="Thiếu hoặc sai API key (header X-API-Key).",
            headers={"WWW-Authenticate": "Bearer"},
        )
