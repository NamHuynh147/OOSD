"""Trình chạy migration SQL thuần (psycopg 3 — không ORM, không Alembic).

    python -m app.db.migrate             # tạo vai trò + áp dụng các migration còn thiếu
    python -m app.db.migrate --status    # liệt kê trạng thái, không thay đổi gì
    python -m app.db.migrate --seed      # như trên, rồi nạp kho tài liệu mẫu

Chạy bằng vai trò OWNER (OWNER_DATABASE_URL): sở hữu schema ``aik08`` và tạo được vai trò đăng nhập.

* Mỗi tệp ``NNN_ten.sql`` chạy trong MỘT giao dịch cùng dòng ghi nhận ở ``aik08.schema_migrations``;
  lỗi giữa chừng thì không còn dấu vết nào (DDL của PostgreSQL có tính giao dịch).
* Checksum được lưu để phát hiện việc sửa migration đã áp dụng — hãy tạo migration mới.
* ``NNN_ten.optional.sql`` là TÙY CHỌN (vd. pgvector cần siêu người dùng): lỗi thì bỏ qua, ghi vào báo
  cáo và thử lại ở lần chạy sau.
* Placeholder ``__READER_ROLE__`` / ``__APP_ROLE__`` được thay bằng tên vai trò thật.
* Khóa advisory ngăn hai tiến trình migrate đồng thời.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import psycopg
from psycopg import errors as pg_errors
from psycopg import sql
from psycopg.conninfo import conninfo_to_dict

from app.config import DEFAULT_APP_DSN, DEFAULT_READER_DSN, Settings
from app.errors import ConfigurationError

MIGRATIONS_DIR = Path(__file__).parent / "migrations"
SCHEMA = "aik08"
_LOCK_KEY = 0x41494B30  # "AIK0": khóa advisory, tránh hai tiến trình migrate cùng lúc
_FILE = re.compile(r"^(?P<version>\d{3})_(?P<name>[a-z0-9_]+?)(?P<optional>\.optional)?\.sql$")
_ROLE_NAME = re.compile(r"^[a-z_][a-z0-9_]{0,62}$")

_TRACKING_DDL = f"""
CREATE TABLE IF NOT EXISTS {SCHEMA}.schema_migrations (
    version    text        PRIMARY KEY,
    name       text        NOT NULL,
    checksum   text        NOT NULL,
    applied_at timestamptz NOT NULL DEFAULT now()
)
"""


@dataclass(frozen=True, slots=True)
class Migration:
    version: str
    name: str
    sql: str
    checksum: str
    optional: bool


@dataclass(frozen=True, slots=True)
class RoleConfig:
    """Tên + mật khẩu của hai vai trò đăng nhập (đặc quyền tối thiểu)."""

    reader: str = "aik08_reader"
    app: str = "aik08_app"
    reader_password: str | None = None
    app_password: str | None = None

    def __post_init__(self) -> None:
        for name in (self.reader, self.app):
            if not _ROLE_NAME.match(name):
                raise ConfigurationError(f"Tên vai trò CSDL không hợp lệ: {name!r}")
        if self.reader == self.app:
            raise ConfigurationError("Vai trò reader và app phải khác nhau (tách quyền đọc/ghi).")

    @classmethod
    def from_dsns(cls, reader_dsn: str, app_dsn: str) -> RoleConfig:
        reader, app = conninfo_to_dict(reader_dsn), conninfo_to_dict(app_dsn)
        return cls(
            reader=str(reader.get("user") or "aik08_reader"),
            app=str(app.get("user") or "aik08_app"),
            reader_password=reader.get("password"),
            app_password=app.get("password"),
        )

    @classmethod
    def from_settings(cls, settings: Settings) -> RoleConfig:
        return cls.from_dsns(settings.reader_dsn or DEFAULT_READER_DSN, settings.app_dsn or DEFAULT_APP_DSN)


@dataclass(slots=True)
class MigrationReport:
    applied: list[str] = field(default_factory=list)
    skipped: list[tuple[str, str]] = field(default_factory=list)  # (phiên bản, lý do) — migration tùy chọn
    roles_created: list[str] = field(default_factory=list)


def discover(directory: Path = MIGRATIONS_DIR) -> list[Migration]:
    migrations: list[Migration] = []
    for path in sorted(directory.iterdir()):
        match = _FILE.match(path.name)
        if not match:
            continue
        text = path.read_text(encoding="utf-8")
        migrations.append(
            Migration(
                version=match["version"],
                name=match["name"],
                sql=text,
                checksum=hashlib.sha256(text.encode("utf-8")).hexdigest(),
                optional=bool(match["optional"]),
            )
        )
    versions = [m.version for m in migrations]
    if len(versions) != len(set(versions)):
        raise ConfigurationError(f"Trùng số phiên bản migration trong {directory}")
    return migrations


def render(text: str, roles: RoleConfig) -> str:
    """Thay placeholder tên vai trò (đã kiểm tra là định danh an toàn) bằng tên thật."""
    return text.replace("__READER_ROLE__", roles.reader).replace("__APP_ROLE__", roles.app)


def _ensure_roles(conn: psycopg.Connection, roles: RoleConfig) -> list[str]:
    created: list[str] = []
    for name, password in ((roles.reader, roles.reader_password), (roles.app, roles.app_password)):
        if conn.execute("SELECT 1 FROM pg_roles WHERE rolname = %s", (name,)).fetchone():
            continue
        stmt: sql.Composable = sql.SQL("CREATE ROLE {} LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION").format(
            sql.Identifier(name)
        )
        if password:
            stmt = stmt + sql.SQL(" PASSWORD {}").format(sql.Literal(password))
        try:
            conn.execute(stmt)
        except pg_errors.InsufficientPrivilege as exc:
            raise ConfigurationError(
                f"Vai trò '{name}' chưa tồn tại và tài khoản owner không có quyền CREATEROLE. "
                "Nhờ quản trị viên tạo vai trò (LOGIN, không siêu người dùng) rồi chạy lại."
            ) from exc
        created.append(name)
    return created


def _applied(conn: psycopg.Connection) -> dict[str, str]:
    rows = conn.execute(f"SELECT version, checksum FROM {SCHEMA}.schema_migrations").fetchall()
    return {r[0]: r[1] for r in rows}


def apply_migrations(
    owner_dsn: str,
    roles: RoleConfig | None = None,
    directory: Path = MIGRATIONS_DIR,
) -> MigrationReport:
    """Tạo vai trò (nếu thiếu) và áp dụng các migration chưa chạy."""
    roles = roles or RoleConfig()
    migrations = discover(directory)
    if not migrations:
        raise ConfigurationError(f"Không tìm thấy migration nào trong {directory}")

    report = MigrationReport()
    with psycopg.connect(owner_dsn, autocommit=True) as conn:
        conn.execute("SELECT pg_advisory_lock(%s)", (_LOCK_KEY,))
        try:
            conn.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA}")
            conn.execute(_TRACKING_DDL)
            report.roles_created = _ensure_roles(conn, roles)
            done = _applied(conn)
            for m in migrations:
                if m.version in done:
                    if done[m.version] != m.checksum:
                        raise ConfigurationError(
                            f"Migration {m.version}_{m.name} đã áp dụng nhưng nội dung đã bị sửa "
                            "(checksum khác). Hãy tạo migration mới thay vì sửa migration cũ."
                        )
                    continue
                try:
                    with conn.transaction():
                        conn.execute(render(m.sql, roles))  # không tham số => cho phép nhiều câu lệnh
                        conn.execute(
                            f"INSERT INTO {SCHEMA}.schema_migrations (version, name, checksum) VALUES (%s, %s, %s)",
                            (m.version, m.name, m.checksum),
                        )
                except psycopg.Error as exc:
                    if not m.optional:
                        raise
                    reason = (exc.diag.message_primary or str(exc)).splitlines()[0]
                    report.skipped.append((m.version, reason))
                    continue
                report.applied.append(m.version)
        finally:
            conn.execute("SELECT pg_advisory_unlock(%s)", (_LOCK_KEY,))
    return report


def status(owner_dsn: str, directory: Path = MIGRATIONS_DIR) -> list[tuple[str, str, bool, bool]]:
    """(phiên bản, tên, đã áp dụng?, tùy chọn?) — chỉ đọc, không tạo đối tượng nào."""
    with psycopg.connect(owner_dsn, autocommit=True) as conn:
        exists = conn.execute(f"SELECT to_regclass('{SCHEMA}.schema_migrations')").fetchone()
        done = _applied(conn) if exists and exists[0] else {}
    return [(m.version, m.name, m.version in done, m.optional) for m in discover(directory)]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Chạy migration SQL cho AIK-08")
    parser.add_argument("--status", action="store_true", help="chỉ liệt kê trạng thái")
    parser.add_argument("--seed", action="store_true", help="nạp kho tài liệu mẫu sau khi migrate")
    args = parser.parse_args(argv)

    settings = Settings.from_env()
    if args.status:
        for version, name, applied, optional in status(settings.owner_dsn):
            tag = " (tùy chọn)" if optional else ""
            print(f"{'[x]' if applied else '[ ]'} {version}_{name}{tag}")
        return 0

    report = apply_migrations(settings.owner_dsn, RoleConfig.from_settings(settings))
    for role in report.roles_created:
        print(f"Đã tạo vai trò đăng nhập: {role}")
    for version, reason in report.skipped:
        print(f"Bỏ qua migration tùy chọn {version}: {reason}")
    print("Đã áp dụng: " + ", ".join(report.applied) if report.applied else "CSDL đã ở phiên bản mới nhất.")

    if args.seed:
        from app.db.seed import seed

        print(f"Đã nạp {seed(settings.owner_dsn)} tài liệu mẫu.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
