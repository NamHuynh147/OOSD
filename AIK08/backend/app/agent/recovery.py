"""Đóng các phiên mồ côi: tiến trình chết giữa chừng, hoặc phiên pending/running quá hạn.

Không có việc này, một phiên đang chạy mà tiến trình bị tắt sẽ nằm ở ``running`` mãi (và nếu người dùng
bấm Hủy thì ở ``cancelling`` mãi) mà không có báo cáo. ``AgentOrchestrator.recover`` ghi báo cáo từ bằng
chứng đã lưu: ``cancelled`` nếu người dùng đã yêu cầu hủy, ``failed`` nếu không.

* Khi khởi động (``force=True``) mọi phiên chưa kết thúc đều là mồ côi — giả định MỘT tiến trình API.
  Nếu chạy nhiều worker, đặt ``RECOVER_ON_START=false`` và chỉ dựa vào bộ quét theo tuổi bên dưới.
* Bộ quét định kỳ chỉ đóng phiên đã quá ``max_seconds + orphan_grace_seconds`` kể từ lúc bắt đầu.
"""

from __future__ import annotations

import logging
import threading
from datetime import UTC, datetime

from app.agent.orchestrator import AgentOrchestrator
from app.config import Settings
from app.core.models import SessionRecord, SessionStatus
from app.db.sessions import SessionRepository

log = logging.getLogger(__name__)


class SessionRecovery:
    def __init__(self, sessions: SessionRepository, orchestrator: AgentOrchestrator, settings: Settings) -> None:
        self._sessions = sessions
        self._orchestrator = orchestrator
        self._settings = settings
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

    def is_orphan(self, session: SessionRecord, *, now: datetime | None = None) -> bool:
        grace = self._settings.orphan_grace_seconds
        if session.status is SessionStatus.PENDING:
            age = ((now or datetime.now(UTC)) - session.created_at).total_seconds()
            return age > session.limits.max_seconds + grace
        return session.usage.seconds > session.limits.max_seconds + grace

    def recover_all(self, *, force: bool = False) -> int:
        """Đóng các phiên mồ côi; trả về số phiên đã đóng."""
        closed = 0
        for session in self._sessions.list_unfinished():
            if not force and not self.is_orphan(session):
                continue
            try:
                if self._orchestrator.recover(session.id) is not None:
                    closed += 1
                    log.warning("Đã đóng phiên mồ côi %s (trạng thái cũ: %s)", session.id, session.status.value)
            except Exception:  # noqa: BLE001 — một phiên lỗi không được chặn các phiên khác
                log.exception("Không đóng được phiên mồ côi %s", session.id)
        return closed

    def start(self) -> None:
        if self._thread is not None:
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self._loop, name="aik08-session-sweeper", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=5)
            self._thread = None

    def _loop(self) -> None:
        while not self._stop.wait(self._settings.sweep_interval_seconds):
            try:
                self.recover_all()
            except Exception:  # noqa: BLE001
                log.exception("Bộ quét phiên mồ côi gặp lỗi")
