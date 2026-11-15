"""Công cụ HTTP GET có giới hạn chặt: allowlist theo TIỀN TỐ URL đầy đủ, không redirect, chỉ nhận JSON/văn bản,
giới hạn dung lượng và tổng thời gian. Không có phương thức ghi, không header/body tùy ý."""

from __future__ import annotations

import ipaddress
import json
import time
from typing import Any
from urllib.parse import unquote, urlparse

import httpx

from app.errors import InvalidToolArgumentsError, ToolExecutionError
from app.tools.base import ToolResult

ALLOWED_CONTENT_TYPES = ("application/json", "text/plain", "text/markdown", "text/csv")
_DEFAULT_PORTS = {"http": 80, "https": 443}


def _origin(parsed) -> tuple[str, str, int]:
    scheme = parsed.scheme.lower()
    return scheme, (parsed.hostname or "").lower().rstrip("."), parsed.port or _DEFAULT_PORTS.get(scheme, 0)


def _under(path: str, prefix_path: str) -> bool:
    if prefix_path.endswith("/"):
        return path.startswith(prefix_path)  # tiền tố là một thư mục: chỉ nhận thứ nằm BÊN TRONG
    return path == prefix_path or path.startswith(prefix_path + "/")


class HttpGetApiTool:
    name = "http_get_api"
    description = (
        "Gọi API bằng HTTP GET tới URL nằm trong allowlist tiền tố (ví dụ /demo/...). "
        "Tham số: url (str). Chỉ đọc; chỉ nhận JSON hoặc văn bản."
    )

    def __init__(
        self,
        *,
        allowed_prefixes: tuple[str, ...],
        timeout_seconds: float = 8.0,
        max_bytes: int = 200_000,
        client: httpx.Client | None = None,
    ) -> None:
        self._prefixes = []
        for raw in allowed_prefixes:
            parsed = urlparse(raw)
            if parsed.scheme not in {"http", "https"} or not parsed.hostname or parsed.query or parsed.fragment:
                raise ValueError(f"Tiền tố URL không hợp lệ: {raw!r}")
            self._prefixes.append((_origin(parsed), parsed.path or "/"))
        self._timeout = max(0.1, timeout_seconds)
        self._max_bytes = max(1_024, max_bytes)
        self._client = client
        self._owns_client = client is None

    def close(self) -> None:
        """Đóng client HTTP do công cụ tự tạo (gọi khi phiên kết thúc)."""
        if self._owns_client and self._client is not None:
            self._client.close()
            self._client = None

    def _validate_url(self, value: Any) -> str:
        if not isinstance(value, str) or len(value) > 2_048:
            raise InvalidToolArgumentsError("url phải là chuỗi tối đa 2.048 ký tự")
        if any(ch in value for ch in "\\\r\n\t ") or any(ord(ch) < 32 for ch in value):
            raise InvalidToolArgumentsError("URL chứa ký tự không hợp lệ")
        parsed = urlparse(value)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            raise InvalidToolArgumentsError("Chỉ chấp nhận URL HTTP(S) tuyệt đối")
        if parsed.username or parsed.password or parsed.fragment:
            raise InvalidToolArgumentsError("URL không được chứa thông tin đăng nhập hoặc fragment")
        decoded = unquote(unquote(parsed.path))  # chặn cả mã hóa kép của ../ và \
        if ".." in decoded.split("/") or "\\" in decoded:
            raise InvalidToolArgumentsError("Đường dẫn URL không được chứa '..'")
        origin = _origin(parsed)
        if not any(
            origin == allowed_origin and _under(parsed.path or "/", prefix_path)
            for allowed_origin, prefix_path in self._prefixes
        ):
            raise InvalidToolArgumentsError("URL không nằm trong API_ALLOWED_URL_PREFIXES")
        try:
            ip = ipaddress.ip_address(origin[1])
            if not (ip.is_global or ip.is_loopback):
                raise InvalidToolArgumentsError("Không cho phép địa chỉ IP private/link-local")
        except ValueError:
            pass
        return value

    def validate(self, arguments: dict[str, Any]) -> str:
        url = self._validate_url(arguments.get("url"))
        if set(arguments) - {"url"}:
            raise InvalidToolArgumentsError("http_get_api chỉ nhận tham số url")
        return url

    def execute(self, arguments: dict[str, Any]) -> ToolResult:
        url = self.validate(arguments)
        if self._client is None:
            self._client = httpx.Client(
                timeout=self._timeout,
                follow_redirects=False,
                headers={"Accept": "application/json, text/plain, text/markdown"},
            )
        deadline = time.monotonic() + self._timeout  # httpx chỉ giới hạn từng lần đọc; đây là tổng thời gian
        try:
            with self._client.stream("GET", url, timeout=self._timeout) as response:
                if 300 <= response.status_code < 400:
                    raise ToolExecutionError("API redirect bị chặn")
                response.raise_for_status()
                content_type = response.headers.get("content-type", "")
                mime = content_type.split(";")[0].strip().lower()
                if mime not in ALLOWED_CONTENT_TYPES and not mime.endswith("+json"):
                    raise ToolExecutionError(f"Content-Type không được hỗ trợ: {mime or '(trống)'}")
                declared = response.headers.get("content-length", "")
                if declared.isdigit() and int(declared) > self._max_bytes:
                    raise ToolExecutionError(f"Phản hồi API vượt giới hạn {self._max_bytes} byte")
                chunks: list[bytes] = []
                size = 0
                for chunk in response.iter_bytes():
                    size += len(chunk)
                    if size > self._max_bytes:
                        raise ToolExecutionError(f"Phản hồi API vượt giới hạn {self._max_bytes} byte")
                    if time.monotonic() > deadline:
                        raise ToolExecutionError("Phản hồi API vượt tổng thời gian cho phép")
                    chunks.append(chunk)
                text = b"".join(chunks).decode(response.encoding or "utf-8", errors="replace")
                parsed: Any = text
                if "json" in mime:
                    try:
                        parsed = json.loads(text)
                    except json.JSONDecodeError:
                        parsed = text
                content = json.dumps(parsed, ensure_ascii=False, default=str) if not isinstance(parsed, str) else parsed
                data = [
                    {
                        "title": f"GET {url}",
                        "source_uri": url,
                        "content": content,
                        "status_code": response.status_code,
                        "content_type": content_type,
                    }
                ]
                return ToolResult(self.name, data, f"HTTP GET thành công (status {response.status_code}).")
        except ToolExecutionError:
            raise
        except httpx.HTTPError as exc:
            raise ToolExecutionError(f"HTTP GET thất bại: {type(exc).__name__}") from exc
        except (UnicodeError, ValueError) as exc:
            raise ToolExecutionError("Không giải mã được phản hồi API") from exc
