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
    if tag is not None:
        validate_tag(tag, version)
    return version


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate coordinated modelctl package versions and release tags."
    )
    parser.add_argument("--tag", help="Release tag to validate, for example v0.1.0")
    parser.add_argument(
        "--print-version",
        action="store_true",
        help="Print only the coordinated package version.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(__file__).resolve().parents[1]

    try:
        version = validate_release(root, args.tag)
    except (OSError, KeyError, ReleaseValidationError) as error:
        print(f"release validation failed: {error}")
        return 1

    if args.print_version:
        print(version)
    elif args.tag:
        print(f"release tag {args.tag} matches package version {version}")
    else:
        print(f"package versions are coordinated at {version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
