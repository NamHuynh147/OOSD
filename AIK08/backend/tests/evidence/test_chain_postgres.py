"""Chuỗi băm bằng chứng: công thức Python khớp CSDL, và sửa/xóa/chèn lậu đều bị phát hiện hoặc bị chặn."""

import psycopg
import pytest

from app.core.models import Limits
from app.evidence.hashing import ZERO_HASH, chain_hash, sha256_hex
from tests.support import FINISH, ScriptedLLM, act

pytestmark = pytest.mark.postgres


@pytest.fixture
def session_with_evidence(sessions, make_orchestrator):
    llm = ScriptedLLM([act("search_documents", query="sao lưu"), act("search_documents", query="mật khẩu"), FINISH])
    session = sessions.create("quy định sao lưu và mật khẩu", Limits(10, 20000, 60))
    make_orchestrator(llm).run(session.id)
    assert len(sessions.evidence_store(session.id)) >= 2
    return session


def test_python_formula_matches_database_chain(sessions, session_with_evidence):
    items = sessions.evidence_store(session_with_evidence.id).all()
    prev = ZERO_HASH
    for e in items:
        assert e.prev_hash == prev
        assert e.content_sha256 == sha256_hex(e.content)
        assert e.chain_hash == chain_hash(prev, e.seq, e.step_no, e.source_uri, e.raw_sha256, e.content_sha256)
        prev = e.chain_hash
    assert sessions.evidence_store(session_with_evidence.id).verify_integrity().ok


@pytest.mark.parametrize(
    "sql",
    [
        "UPDATE aik08.evidence SET content = 'x' WHERE session_id = %s",
        "DELETE FROM aik08.evidence WHERE session_id = %s",
    ],
)
def test_app_and_owner_cannot_modify_or_delete_evidence(pg, session_with_evidence, sql):
    for dsn in (pg.app, pg.owner):
        with psycopg.connect(dsn, autocommit=True) as conn, pytest.raises(psycopg.Error):
            conn.execute(sql, (session_with_evidence.id,))


def test_tampering_with_triggers_disabled_is_detected_by_verification(pg, sessions, session_with_evidence):
    """Kẻ có quyền siêu người dùng tắt trigger rồi sửa nội dung: lần kiểm chứng kế tiếp phải báo hỏng đúng mục."""
    with psycopg.connect(pg.owner, autocommit=True) as conn:
        conn.execute("SET session_replication_role = replica")
        conn.execute(
            "UPDATE aik08.evidence SET content = 'bị sửa' WHERE session_id = %s AND seq = 1",
            (session_with_evidence.id,),
        )
    report = sessions.evidence_store(session_with_evidence.id).verify_integrity()
    assert not report.ok and 1 in report.broken
