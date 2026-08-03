from __future__ import annotations

import argparse
import re
import tomllib
from pathlib import Path

PACKAGE_PROJECT_FILES = (
    Path("apps/modelctl/pyproject.toml"),
    Path("packages/core/pyproject.toml"),
    Path("packages/sdk/pyproject.toml"),
)
RELEASE_MANIFEST_FILE = Path("release.toml")
REQUIRED_RELEASE_FILES = (
    Path("README.md"),
    Path("README.ko.md"),
    Path("CHANGELOG.md"),
    Path("SECURITY.md"),
    Path("docs/RELEASE_CRITERIA.md"),
    Path("docs/RELEASING.md"),
)
SUPPORTED_RELEASE_STATUSES = {"draft", "ready", "released"}
VERSION_PATTERN = re.compile(
    r"^[0-9]+\.[0-9]+\.[0-9]+(?:(?:a|b|rc)[0-9]+|\.post[0-9]+|\.dev[0-9]+)?$"
)


class ReleaseValidationError(ValueError):
    """Raised when package metadata is not ready for a coordinated release."""


def read_package_versions(root: Path) -> dict[str, str]:
    versions: dict[str, str] = {}

    for relative_path in PACKAGE_PROJECT_FILES:
        path = root / relative_path
        with path.open("rb") as file:
            project = tomllib.load(file)["project"]

        name = project.get("name")
        version = project.get("version")
        if not isinstance(name, str) or not isinstance(version, str):
            raise ReleaseValidationError(
                f"Missing project name or version in {relative_path.as_posix()}"
            )
        versions[name] = version

    return versions


def read_release_manifest(root: Path) -> dict[str, object]:
    path = root / RELEASE_MANIFEST_FILE
    with path.open("rb") as file:
        manifest = tomllib.load(file)

    if not isinstance(manifest, dict):
        raise ReleaseValidationError("release.toml must contain a TOML table")
    return manifest


def validate_package_versions(versions: dict[str, str]) -> str:
    unique_versions = set(versions.values())
    if len(unique_versions) != 1:
        details = ", ".join(
            f"{name}={version}" for name, version in sorted(versions.items())
        )
        raise ReleaseValidationError(f"Package versions do not match: {details}")

    version = next(iter(unique_versions))
    if VERSION_PATTERN.fullmatch(version) is None:
        raise ReleaseValidationError(f"Unsupported release version: {version}")

    return version


def validate_release_manifest(manifest: dict[str, object], version: str) -> str:
    manifest_version = manifest.get("version")
    if manifest_version != version:
        raise ReleaseValidationError(
            f"Release manifest version {manifest_version!r} does not match package "
            f"version {version!r}"
        )

    status = manifest.get("status")
    if not isinstance(status, str) or status not in SUPPORTED_RELEASE_STATUSES:
        supported = ", ".join(sorted(SUPPORTED_RELEASE_STATUSES))
        raise ReleaseValidationError(
            f"Unsupported release status {status!r}; expected one of: {supported}"
        )

    channel = manifest.get("channel")
    if channel != "development":
        raise ReleaseValidationError(
            f"Unsupported release channel {channel!r}; expected 'development'"
        )

    if manifest.get("publish_pypi") is not False:
        raise ReleaseValidationError(
            "PyPI publication must remain disabled in release.toml"
        )

    return status


def validate_release_documents(root: Path, version: str, status: str) -> None:
    missing = [
        path.as_posix() for path in REQUIRED_RELEASE_FILES if not (root / path).is_file()
    ]
    if missing:
        raise ReleaseValidationError(
            f"Missing required release files: {', '.join(missing)}"
        )

    changelog = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    changelog_heading = re.compile(
        rf"^## \[{re.escape(version)}\](?:\s+-\s+\d{{4}}-\d{{2}}-\d{{2}})?$",
        re.MULTILINE,
    )
    if changelog_heading.search(changelog) is None:
        raise ReleaseValidationError(
            f"CHANGELOG.md does not contain a release heading for {version}"
        )

    criteria = (root / "docs/RELEASE_CRITERIA.md").read_text(encoding="utf-8")
    if f"Version: `{version}`" not in criteria:
        raise ReleaseValidationError(
            f"docs/RELEASE_CRITERIA.md does not identify version {version}"
        )

    expected_status = status.capitalize()
    if f"Status: **{expected_status}**" not in criteria:
        raise ReleaseValidationError(
            "docs/RELEASE_CRITERIA.md status does not match release.toml"
        )


def validate_tag(tag: str, version: str) -> None:
    expected = f"v{version}"
    if tag != expected:
        raise ReleaseValidationError(
            f"Release tag {tag!r} does not match package version {version!r}; "
            f"expected {expected!r}"
        )


def validate_release(root: Path, tag: str | None = None) -> str:
    versions = read_package_versions(root)
    version = validate_package_versions(versions)
    manifest = read_release_manifest(root)
    status = validate_release_manifest(manifest, version)
    validate_release_documents(root, version, status)
    if tag is not None:
        validate_tag(tag, version)
    return version


def release_status(root: Path) -> str:
    versions = read_package_versions(root)
    version = validate_package_versions(versions)
    manifest = read_release_manifest(root)
    return validate_release_manifest(manifest, version)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate coordinated modelctl package versions and release readiness."
    )
    parser.add_argument("--tag", help="Release tag to validate, for example v0.1.0")
    output = parser.add_mutually_exclusive_group()
    output.add_argument(
        "--print-version",
        action="store_true",
        help="Print only the coordinated package version.",
    )
    output.add_argument(
        "--print-status",
        action="store_true",
        help="Print only the release readiness status.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(__file__).resolve().parents[1]

    try:
        version = validate_release(root, args.tag)
        status = release_status(root)
    except (OSError, KeyError, tomllib.TOMLDecodeError, ReleaseValidationError) as error:
        print(f"release validation failed: {error}")
        return 1

    if args.print_version:
        print(version)
    elif args.print_status:
        print(status)
    elif args.tag:
        print(
            f"release tag {args.tag} matches package version {version} "
            f"with status {status}"
        )
    else:
        print(f"release {version} is coordinated with status {status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
