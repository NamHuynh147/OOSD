"""T4 — phiên mồ côi (tiến trình chết) vẫn được đóng và có báo cáo."""

from __future__ import annotations

import dataclasses
from datetime import UTC, datetime, timedelta

import pytest

from app.agent.recovery import SessionRecovery
from app.core.models import Limits, SessionStatus, StopReason
from tests.support import HookedMock

pytestmark = pytest.mark.postgres


def _recovery(orch, sessions, settings, **kw):
    return SessionRecovery(sessions, orch, dataclasses.replace(settings, **kw))


def _make_running(sessions, query="phiên mồ côi", limits=Limits(5, 5000, 5)):
    s = sessions.create(query, limits)
    assert sessions.mark_running(s.id)
    return s


def test_recover_running_session_becomes_failed_with_report(sessions, make_orchestrator):
    s = _make_running(sessions)
    report = make_orchestrator(HookedMock()).recover(s.id)
    final = sessions.get(s.id)
    assert final.status is SessionStatus.FAILED and final.stop_reason is StopReason.ERROR
    assert report is not None and report.generated_by == "extractive"
    assert any("gián đoạn" in w for w in report.warnings)


def test_recover_cancelling_session_becomes_cancelled(sessions, make_orchestrator):
    s = _make_running(sessions)
    sessions.request_cancel(s.id)
    assert sessions.get(s.id).status is SessionStatus.CANCELLING
    make_orchestrator(HookedMock()).recover(s.id)
    final = sessions.get(s.id)
    assert final.status is SessionStatus.CANCELLED and final.stop_reason is StopReason.CANCELLED_BY_USER


def test_recover_pending_session(sessions, make_orchestrator):
    s = sessions.create("pending mồ côi", Limits(5, 5000, 5))
    make_orchestrator(HookedMock()).recover(s.id)
    assert sessions.get(s.id).status.is_terminal
    assert sessions.get_report(s.id) is not None


def test_recover_is_noop_on_finished_session_and_idempotent(sessions, make_orchestrator):
    s = _make_running(sessions)
    orch = make_orchestrator(HookedMock())
    first = orch.recover(s.id)
    assert first is not None
    assert orch.recover(s.id) is None
    assert sessions.get_report(s.id) == first


def test_force_recover_closes_all_unfinished(sessions, make_orchestrator, settings):
    ids = [_make_running(sessions).id for _ in range(3)]
    ids.append(sessions.create("pending", Limits(5, 5000, 5)).id)
    rec = _recovery(make_orchestrator(HookedMock()), sessions, settings)
    assert rec.recover_all(force=True) >= 4
    assert all(sessions.get(i).status.is_terminal for i in ids)
    assert sessions.list_unfinished() == []


def test_sweep_by_age_only_closes_old_sessions(sessions, make_orchestrator, settings, owner_conn):
    fresh = _make_running(sessions)
    old = _make_running(sessions)
    with owner_conn.transaction():  # chỉnh đồng hồ phiên cũ: bỏ qua trigger bằng vai trò replica (siêu người dùng)
        owner_conn.execute("SET LOCAL session_replication_role = replica")
        owner_conn.execute(
            "UPDATE aik08.agent_sessions SET created_at = now() - interval '700 seconds', "
            "started_at = now() - interval '600 seconds' WHERE id = %s",
            (old.id,),
        )
    rec = _recovery(make_orchestrator(HookedMock()), sessions, settings, orphan_grace_seconds=30.0)
    assert rec.is_orphan(sessions.get(old.id)) and not rec.is_orphan(sessions.get(fresh.id))
    rec.recover_all()
    assert sessions.get(old.id).status.is_terminal
    assert sessions.get(fresh.id).status is SessionStatus.RUNNING
    make_orchestrator(HookedMock()).recover(fresh.id)  # dọn để các test khác không thấy phiên dở


def test_pending_is_orphan_only_after_deadline(sessions, make_orchestrator, settings):
    s = sessions.create("pending", Limits(5, 5000, 5))
    rec = _recovery(make_orchestrator(HookedMock()), sessions, settings, orphan_grace_seconds=30.0)
    assert not rec.is_orphan(s)
    assert rec.is_orphan(s, now=datetime.now(UTC) + timedelta(seconds=120))
    make_orchestrator(HookedMock()).recover(s.id)
