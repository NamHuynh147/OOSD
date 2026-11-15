"""API key: fail-closed khi thiếu cấu hình, từ chối thiếu/sai khóa, /health và /demo mở, khóa hợp lệ chạy được cả luồng."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.api.auth import key_is_valid
from app.config import Settings

KEY = "k_test_0123456789abcdef"
OTHER = "k_other_fedcba9876543210"


def test_key_is_valid_matches_any_configured_key_only():
    assert key_is_valid(KEY, (KEY, OTHER))
    assert key_is_valid(OTHER, (KEY, OTHER))
    assert not key_is_valid("sai", (KEY,))
    assert not key_is_valid("", (KEY,))
    assert not key_is_valid("", ("",))  # khóa rỗng không bao giờ hợp lệ
    assert not key_is_valid(KEY + "x", (KEY,))
    assert not key_is_valid(KEY[:-1], (KEY,))


def test_settings_fail_closed_without_keys():
    with pytest.raises(RuntimeError, match="API_KEYS"):
        Settings().validate_auth()
    with pytest.raises(RuntimeError, match="16"):
        Settings(api_keys=("ngan",)).validate_auth()
    Settings(api_keys=(KEY,)).validate_auth()
    Settings(api_auth_disabled=True).validate_auth()


def test_settings_reads_keys_from_env(monkeypatch):
    monkeypatch.setenv("API_KEYS", f" {KEY} , {OTHER} ")
    monkeypatch.setenv("API_AUTH_DISABLED", "false")
    s = Settings.from_env()
    assert s.api_keys == (KEY, OTHER) and not s.api_auth_disabled


@pytest.fixture
def client(pg, monkeypatch):
    from app.api.main import app

    monkeypatch.setenv("OWNER_DATABASE_URL", pg.owner)
    monkeypatch.setenv("READER_DATABASE_URL", pg.reader)
    monkeypatch.setenv("APP_DATABASE_URL", pg.app)
    monkeypatch.setenv("LLM_PROVIDER", "mock")
    monkeypatch.setenv("API_KEYS", f"{KEY},{OTHER}")
    monkeypatch.delenv("API_AUTH_DISABLED", raising=False)
    monkeypatch.setenv("RECOVER_ON_START", "false")
    with TestClient(app, base_url="http://127.0.0.1:8000") as c:
        yield c


@pytest.mark.postgres
def test_protected_routes_reject_missing_or_wrong_key(client):
    for method, path in [
        ("get", "/api/sessions"),
        ("post", "/api/sessions"),
        ("get", "/api/sessions/00000000-0000-0000-0000-000000000000"),
        ("post", "/api/sessions/00000000-0000-0000-0000-000000000000/cancel"),
        ("get", "/api/sessions/00000000-0000-0000-0000-000000000000/evidence"),
    ]:
        r = getattr(client, method)(path)
        assert r.status_code == 401, (method, path)
        assert r.headers["www-authenticate"] == "Bearer"
        wrong = getattr(client, method)(path, headers={"X-API-Key": "khong-dung-khong-dung"})
        assert wrong.status_code == 401
        assert KEY not in wrong.text and OTHER not in wrong.text


@pytest.mark.postgres
def test_open_routes_need_no_key(client):
    assert client.get("/health").json()["status"] == "ok"
    assert client.get("/demo/status").status_code == 200


@pytest.mark.postgres
def test_valid_key_header_or_bearer_runs_full_flow(client):
    r = client.post(
        "/api/sessions", json={"query": "Cam kết SLA của dịch vụ thanh toán là bao nhiêu?"}, headers={"X-API-Key": KEY}
    )
    assert r.status_code == 202
    sid = r.json()["session"]["id"]
    for headers in ({"X-API-Key": OTHER}, {"Authorization": f"Bearer {KEY}"}):
        assert client.get(f"/api/sessions/{sid}", headers=headers).status_code == 200
        assert client.get(f"/api/sessions/{sid}/evidence", headers=headers).status_code == 200
    assert client.get("/api/sessions", headers={"Authorization": f"Basic {KEY}"}).status_code == 401


@pytest.mark.postgres
def test_app_refuses_to_start_without_keys(pg, monkeypatch):
    from app.api.main import app

    monkeypatch.setenv("OWNER_DATABASE_URL", pg.owner)
    monkeypatch.setenv("READER_DATABASE_URL", pg.reader)
    monkeypatch.setenv("APP_DATABASE_URL", pg.app)
    monkeypatch.setenv("API_KEYS", "")
    monkeypatch.delenv("API_AUTH_DISABLED", raising=False)
    with pytest.raises(RuntimeError, match="API_KEYS"), TestClient(app):
        pass
