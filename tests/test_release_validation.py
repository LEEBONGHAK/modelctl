import sys
from importlib import import_module
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
release_validation = import_module("scripts.release_validation")

ReleaseValidationError = release_validation.ReleaseValidationError
release_status = release_validation.release_status
validate_package_versions = release_validation.validate_package_versions
validate_release = release_validation.validate_release
validate_release_manifest = release_validation.validate_release_manifest
validate_tag = release_validation.validate_tag


def write_project(path: Path, name: str, version: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f'[project]\nname = "{name}"\nversion = "{version}"\n',
        encoding="utf-8",
    )


def write_release_files(
    root: Path,
    *,
    version: str = "0.1.0",
    status: str = "ready",
    publish_pypi: bool = False,
) -> None:
    write_project(root / "pyproject.toml", "modelctl-workspace", version)
    write_project(root / "apps/modelctl/pyproject.toml", "modelctl", version)
    write_project(root / "packages/core/pyproject.toml", "modelctl-core", version)
    write_project(root / "packages/sdk/pyproject.toml", "modelctl-sdk", version)

    root.joinpath("release.toml").write_text(
        "\n".join(
            [
                f'version = "{version}"',
                f'status = "{status}"',
                'channel = "development"',
                f"publish_pypi = {str(publish_pypi).lower()}",
                "",
            ]
        ),
        encoding="utf-8",
    )

    required_text = {
        "README.md": "# modelctl\n",
        "README.ko.md": "# modelctl\n",
        "CHANGELOG.md": f"# Changelog\n\n## [{version}] - 2026-08-03\n",
        "SECURITY.md": "# Security\n",
        "docs/RELEASE_CRITERIA.md": (
            f"# Criteria\n\n- Version: `{version}`\n- Status: **{status.capitalize()}**\n"
        ),
        "docs/RELEASING.md": "# Releasing\n",
    }
    for relative_path, content in required_text.items():
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def test_validate_release_accepts_matching_versions_manifest_docs_and_tag(tmp_path):
    write_release_files(tmp_path)

    assert validate_release(tmp_path, "v0.1.0") == "0.1.0"
    assert release_status(tmp_path) == "ready"


def test_validate_package_versions_rejects_mismatch():
    with pytest.raises(ReleaseValidationError, match="Package versions do not match"):
        validate_package_versions(
            {
                "modelctl": "0.1.0",
                "modelctl-core": "0.1.1",
                "modelctl-sdk": "0.1.0",
            }
        )


def test_validate_release_rejects_manifest_version_mismatch(tmp_path):
    write_release_files(tmp_path)
    tmp_path.joinpath("release.toml").write_text(
        'version = "0.2.0"\nstatus = "ready"\nchannel = "development"\n'
        "publish_pypi = false\n",
        encoding="utf-8",
    )

    with pytest.raises(ReleaseValidationError, match="does not match package version"):
        validate_release(tmp_path)


def test_validate_release_manifest_rejects_pypi_publication():
    with pytest.raises(ReleaseValidationError, match="PyPI publication must remain disabled"):
        validate_release_manifest(
            {
                "version": "0.1.0",
                "status": "ready",
                "channel": "development",
                "publish_pypi": True,
            },
            "0.1.0",
        )


def test_validate_release_rejects_ready_audit_exclusions(tmp_path):
    write_release_files(tmp_path)
    tmp_path.joinpath("pyproject.toml").write_text(
        '[project]\nname = "modelctl-workspace"\nversion = "0.1.0"\n\n'
        '[tool.uv.audit]\nignore = ["GHSA-example"]\n',
        encoding="utf-8",
    )

    with pytest.raises(ReleaseValidationError, match="audit exclusions"):
        validate_release(tmp_path)


def test_validate_release_rejects_missing_changelog_version(tmp_path):
    write_release_files(tmp_path)
    tmp_path.joinpath("CHANGELOG.md").write_text(
        "# Changelog\n\n## [0.0.9] - 2026-08-02\n",
        encoding="utf-8",
    )

    with pytest.raises(ReleaseValidationError, match="release heading for 0.1.0"):
        validate_release(tmp_path)


def test_validate_release_rejects_missing_required_document(tmp_path):
    write_release_files(tmp_path)
    tmp_path.joinpath("SECURITY.md").unlink()

    with pytest.raises(ReleaseValidationError, match="SECURITY.md"):
        validate_release(tmp_path)


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
