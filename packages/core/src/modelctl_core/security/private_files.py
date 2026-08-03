from __future__ import annotations

import os
import tempfile
from pathlib import Path

PRIVATE_DIRECTORY_MODE = 0o700
PRIVATE_FILE_MODE = 0o600


def _reject_symlink(path: Path) -> None:
    if path.is_symlink():
        raise RuntimeError(f"Refusing to access symbolic link: {path}")


def ensure_private_directory(path: Path) -> None:
    _reject_symlink(path)
    path.mkdir(parents=True, exist_ok=True)
    if os.name != "nt":
        path.chmod(PRIVATE_DIRECTORY_MODE)


def harden_private_file(path: Path) -> None:
    _reject_symlink(path)
    if path.exists() and os.name != "nt":
        path.chmod(PRIVATE_FILE_MODE)


def read_private_text(path: Path, *, encoding: str = "utf-8") -> str:
    harden_private_file(path)
    return path.read_text(encoding=encoding)


def atomic_write_private_text(
    path: Path,
    content: str,
    *,
    encoding: str = "utf-8",
) -> None:
    _reject_symlink(path)
    ensure_private_directory(path.parent)

    descriptor, temporary_name = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        text=True,
    )
    temporary_path = Path(temporary_name)

    try:
        if os.name != "nt":
            os.fchmod(descriptor, PRIVATE_FILE_MODE)

        with os.fdopen(descriptor, "w", encoding=encoding) as temporary_file:
            temporary_file.write(content)
            temporary_file.flush()
            os.fsync(temporary_file.fileno())

        os.replace(temporary_path, path)
        harden_private_file(path)
    except BaseException:
        try:
            os.close(descriptor)
        except OSError:
            pass
        temporary_path.unlink(missing_ok=True)
        raise
