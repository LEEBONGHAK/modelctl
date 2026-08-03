import sys
from importlib import import_module
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
release_validation = import_module("scripts.release_validation")

ReleaseValidationError = release_validation.ReleaseValidationError
validate_package_versions = release_validation.validate_package_versions
validate_release = release_validation.validate_release
validate_tag = release_validation.validate_tag


def write_project(path: Path, name: str, version: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f'[project]\nname = "{name}"\nversion = "{version}"\n',
        encoding="utf-8",
    )


def test_validate_release_accepts_matching_versions_and_tag(tmp_path):
    write_project(tmp_path / "apps/modelctl/pyproject.toml", "modelctl", "0.1.0")
    write_project(tmp_path / "packages/core/pyproject.toml", "modelctl-core", "0.1.0")
    write_project(tmp_path / "packages/sdk/pyproject.toml", "modelctl-sdk", "0.1.0")

    assert validate_release(tmp_path, "v0.1.0") == "0.1.0"


def test_validate_package_versions_rejects_mismatch():
    with pytest.raises(ReleaseValidationError, match="Package versions do not match"):
        validate_package_versions(
            {
                "modelctl": "0.1.0",
                "modelctl-core": "0.1.1",
                "modelctl-sdk": "0.1.0",
            }
        )


def test_validate_tag_rejects_version_mismatch():
    with pytest.raises(ReleaseValidationError, match="expected 'v0.1.0'"):
        validate_tag("v0.2.0", "0.1.0")


@pytest.mark.parametrize(
    "tag",
    [
        "v0.1.0\nmalicious=true",
        "v0.1.0; touch injected",
        "$(touch injected)",
        "v0.1.0 ",
    ],
)
def test_validate_tag_rejects_untrusted_input(tag):
    with pytest.raises(ReleaseValidationError):
        validate_tag(tag, "0.1.0")


def test_validate_package_versions_rejects_unsupported_version():
    with pytest.raises(ReleaseValidationError, match="Unsupported release version"):
        validate_package_versions(
            {
                "modelctl": "next",
                "modelctl-core": "next",
                "modelctl-sdk": "next",
            }
        )
