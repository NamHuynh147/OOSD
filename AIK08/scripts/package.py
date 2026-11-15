"""Đóng gói mã nguồn để nộp/gửi: loại bỏ bí mật, thư viện cài sẵn và tệp sinh ra.

    python scripts/package.py [đường-dẫn-zip]      (mặc định: ../aik08-source.zip)

Trong kho git thì dùng `git ls-files` (theo .gitignore); ngoài git thì duyệt thư mục với danh sách
loại trừ bên dưới. Dù thế nào cũng từ chối đóng gói tệp .env và cảnh báo nếu gói quá 1 MB.
"""

from __future__ import annotations

import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".pytest_cache", ".ruff_cache", ".mypy_cache",
             ".venv", "venv", "dist", ".idea", ".vscode"}
SKIP_SUFFIXES = (".pyc", ".pyo", ".zip", ".tsbuildinfo", ".log")


def _is_secret(path: Path) -> bool:
    return path.name == ".env" or (path.name.startswith(".env.") and path.name != ".env.example")


def _git_files() -> list[Path] | None:
    try:
        out = subprocess.run(["git", "ls-files", "-co", "--exclude-standard", "-z"], cwd=ROOT,
                             capture_output=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return None
    return [ROOT / p for p in out.decode("utf-8").split("\0") if p]


def _walk_files() -> list[Path]:
    return [p for p in ROOT.rglob("*")
            if p.is_file() and not (set(p.relative_to(ROOT).parts) & SKIP_DIRS)
            and not p.name.endswith(SKIP_SUFFIXES) and not p.name.endswith(".egg-info")
            and ".egg-info" not in str(p)]


def main() -> int:
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / "aik08-source.zip"
    files = _git_files() if (ROOT / ".git").exists() else None
    files = files if files is not None else _walk_files()
    files = [p for p in files if p.is_file() and not _is_secret(p) and p.resolve() != target.resolve()]
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(files):
            zf.write(path, Path("aik08") / path.relative_to(ROOT))
    size = target.stat().st_size
    print(f"{target}: {len(files)} tệp, {size / 1024:.0f} KB")
    if size > 1_000_000:
        print("CẢNH BÁO: gói lớn hơn 1 MB — kiểm tra lại các thư mục sinh ra.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
