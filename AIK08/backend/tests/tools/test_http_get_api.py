import httpx
import pytest

from app.errors import InvalidToolArgumentsError, ToolExecutionError
from app.tools.http_get_api import HttpGetApiTool

PREFIX = ("http://127.0.0.1:8000/demo/",)
OK = "http://127.0.0.1:8000/demo/status"


def tool(handler=None, **kw) -> HttpGetApiTool:
    client = httpx.Client(transport=httpx.MockTransport(handler)) if handler else None
    return HttpGetApiTool(allowed_prefixes=PREFIX, client=client, **kw)


@pytest.mark.parametrize(
    "url",
    [
        "https://example.com/data",  # host lạ
        "http://127.0.0.1:8000/api/sessions",  # cùng host nhưng ngoài tiền tố (không phải /demo/)
        "http://127.0.0.1:8000/demo",  # chỉ khớp thư mục, không phải tài nguyên
        "http://127.0.0.1:8000/demonstration/x",  # tiền tố chuỗi nhưng khác đoạn đường dẫn
        "http://127.0.0.1:9999/demo/status",  # sai cổng
        "https://127.0.0.1:8000/demo/status",  # sai scheme
        "http://127.0.0.1:8000/demo/../api/sessions",  # leo thư mục
        "http://127.0.0.1:8000/demo/%2e%2e/api/sessions",  # leo thư mục mã hóa
        "http://127.0.0.1:8000/demo/%252e%252e/x",  # mã hóa kép
        "http://127.0.0.1:8000\\@evil.example/demo/x",  # lừa phân tích URL
        "http://user:pw@127.0.0.1:8000/demo/x",  # thông tin đăng nhập
        "http://127.0.0.1:8000/demo/x#frag",
        "file:///etc/passwd",
        "ftp://127.0.0.1/demo/x",
        "",
        None,
        5,
    ],
)
def test_url_outside_allowlist_prefix_is_rejected(url):
    with pytest.raises(InvalidToolArgumentsError):
        tool().validate({"url": url})


def test_allowed_url_and_extra_arguments():
    assert tool().validate({"url": OK}) == OK
    assert tool().validate({"url": OK + "?q=1"}).endswith("q=1")
    with pytest.raises(InvalidToolArgumentsError):
        tool().validate({"url": OK, "method": "DELETE"})


def test_prefix_must_be_valid_url():
    with pytest.raises(ValueError):
        HttpGetApiTool(allowed_prefixes=("localhost/demo",))


def test_json_response_is_returned():
    result = tool(
        lambda r: httpx.Response(200, json={"ok": True}, headers={"content-type": "application/json"})
    ).execute({"url": OK})
    assert result.data[0]["content"] == '{"ok": true}' and result.data[0]["source_uri"] == OK


@pytest.mark.parametrize("ctype", ["text/html", "application/octet-stream", "image/png", ""])
def test_non_json_text_content_types_are_rejected(ctype):
    with pytest.raises(ToolExecutionError, match="Content-Type"):
        tool(lambda r: httpx.Response(200, content=b"x", headers={"content-type": ctype})).execute({"url": OK})


def test_redirect_is_blocked():
    with pytest.raises(ToolExecutionError, match="redirect"):
        tool(lambda r: httpx.Response(302, headers={"location": "http://evil.example/"})).execute({"url": OK})


def test_oversized_body_is_rejected():
    big = httpx.Response(200, content=b"a" * 5_000, headers={"content-type": "text/plain"})
    with pytest.raises(ToolExecutionError, match="giới hạn"):
        tool(lambda r: big, max_bytes=1_024).execute({"url": OK})


def test_total_deadline_is_enforced_on_slow_stream(monkeypatch):
    import app.tools.http_get_api as mod

    clock = iter([0.0] + [100.0] * 20)
    monkeypatch.setattr(mod.time, "monotonic", lambda: next(clock))
    ok = httpx.Response(200, content=b"abc", headers={"content-type": "text/plain"})
    with pytest.raises(ToolExecutionError, match="thời gian"):
        tool(lambda r: ok, timeout_seconds=2).execute({"url": OK})


def test_close_releases_owned_client_only():
    own = HttpGetApiTool(allowed_prefixes=PREFIX)
    own._client = httpx.Client()
    own._owns_client = True
    own.close()
    assert own._client is None
    shared = tool(lambda r: httpx.Response(200))
    shared.close()
    assert shared._client is not None
