"""Kết nối PostgreSQL bằng psycopg 3 + pool — SQL thuần, không ORM.

Hai pool, hai vai trò CSDL khác nhau (nguyên tắc đặc quyền tối thiểu):

  reader  → ``aik08_reader``: chỉ SELECT nguồn tri thức. Dùng cho CÔNG CỤ của agent.
            Ba lớp bảo vệ độc lập: (1) quyền SELECT-only, (2) giao dịch mặc định chỉ-đọc
            đặt ở mức vai trò, (3) tùy chọn kết nối ``default_transaction_read_only=on``.
  app     → ``aik08_app``: ghi sổ phiên (INSERT theo cột + UPDATE hẹp), không đụng nguồn tri thức.

Cả hai dùng autocommit; nhóm câu lệnh cần nguyên tử thì bọc ``with conn.transaction():``.
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

import psycopg
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

from app.config import Settings


class Database:
    def __init__(
        self, *, reader_dsn: str, app_dsn: str, min_size: int = 1, max_size: int = 8
    ) -> None:
        common = {"autocommit": True, "row_factory": dict_row}
        self._reader = ConnectionPool(
            reader_dsn,
            min_size=min_size,
            max_size=max_size,
            kwargs={**common, "options": "-c default_transaction_read_only=on"},
            name="aik08-reader",
            open=False,
        )
        self._app = ConnectionPool(
            app_dsn,
            min_size=min_size,
            max_size=max_size,
            kwargs=dict(common),
            name="aik08-app",
            open=False,
        )

    @classmethod
    def from_settings(cls, settings: Settings, *, max_size: int = 8) -> Database:
        return cls(
            reader_dsn=settings.reader_dsn, app_dsn=settings.app_dsn, max_size=max_size
        )

    def open(self, timeout: float = 10.0) -> None:
        self._reader.open(wait=True, timeout=timeout)
        self._app.open(wait=True, timeout=timeout)

    def close(self) -> None:
        self._reader.close()
        self._app.close()

    @contextmanager
    def reader(self) -> Iterator[psycopg.Connection]:
        """Kết nối chỉ-đọc cho công cụ agent."""
        with self._reader.connection() as conn:
            yield conn

    @contextmanager
    def app(self) -> Iterator[psycopg.Connection]:
        """Kết nối ghi sổ phiên."""
        with self._app.connection() as conn:
            yield conn

    def check_schema(self) -> bool:
        """True nếu lược đồ đã được migrate (bảng allowlist có dữ liệu)."""
        try:
            with self.app() as conn:
                row = conn.execute("SELECT count(*) AS n FROM allowed_tools").fetchone()
            return bool(row and row["n"] > 0)
        except psycopg.Error:
            return False

    def __enter__(self) -> Database:
        self.open()
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()
