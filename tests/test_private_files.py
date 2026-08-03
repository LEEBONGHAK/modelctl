import os

import pytest

from modelctl_core.security.private_files import (
    atomic_write_private_text,
    read_private_text,
)


def test_atomic_private_write_round_trip(tmp_path):
    path = tmp_path / "private" / "secret.json"

    atomic_write_private_text(path, '{"token":"redacted"}\n')

    assert read_private_text(path) == '{"token":"redacted"}\n'
    assert not list(path.parent.glob(f".{path.name}.*.tmp"))


@pytest.mark.skipif(os.name == "nt", reason="POSIX permission bits are not portable")
def test_atomic_private_write_restricts_posix_permissions(tmp_path):
    path = tmp_path / "private" / "secret.json"

    atomic_write_private_text(path, "secret")

    assert path.parent.stat().st_mode & 0o777 == 0o700
    assert path.stat().st_mode & 0o777 == 0o600


def test_private_write_refuses_symbolic_link_target(tmp_path):
    target = tmp_path / "target.txt"
    target.write_text("original", encoding="utf-8")
    link = tmp_path / "link.txt"

    try:
        link.symlink_to(target)
    except (OSError, NotImplementedError):
        pytest.skip("Symbolic links are unavailable")

    with pytest.raises(RuntimeError, match="symbolic link"):
        atomic_write_private_text(link, "replacement")

    assert target.read_text(encoding="utf-8") == "original"
