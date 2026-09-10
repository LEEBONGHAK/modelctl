"""Publish a validated bundle without moving tags or replacing release assets.

Both workflows serialize this script using the same per-tag concurrency group.
Only HTTP 404 means absent; all other lookup failures stop before publication.
"""

from __future__ import annotations

import hashlib
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path


class PublishError(RuntimeError):
    """Publication could not be completed safely."""


class APIError(PublishError):
    def __init__(self, status: int, endpoint: str):
        self.status = status
        super().__init__(f"GitHub API HTTP {status}: {endpoint}")


def gh(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["gh", *args], capture_output=True, text=True, check=False)


def api(endpoint: str, *, method: str = "GET", fields: tuple[str, ...] = ()):
    result = gh("api", "--include", "--method", method, endpoint, *fields)
    headers, separator, body = result.stdout.partition("\n\n")
    match = re.match(r"HTTP/\S+ (\d{3})\b", headers)
    if not separator or match is None:
        raise PublishError(f"No valid HTTP response from GitHub: {endpoint}")
    status = int(match[1])
    if not 200 <= status < 300:
        raise APIError(status, endpoint)
    if result.returncode:
        raise PublishError(f"gh failed after HTTP {status}: {endpoint}")
    try:
        return json.loads(body)
    except ValueError as error:
        raise PublishError(f"Invalid JSON from GitHub: {endpoint}") from error


def optional_api(endpoint: str):
    try:
        return api(endpoint)
    except APIError as error:
        if error.status == 404:
            return None
        raise


def find_release(repository: str, tag: str):
    release = optional_api(f"repos/{repository}/releases/tags/{tag}")
    if release is not None:
        return release
    # The tag endpoint only finds published releases. Enumerate authenticated
    # releases to find a draft left by an interrupted upload, including old pages.
    page = 1
    while True:
        releases = api(f"repos/{repository}/releases?per_page=100&page={page}")
        for candidate in releases:
            if candidate["tag_name"] == tag:
                return candidate
        if len(releases) < 100:
            return None
        page += 1


def tag_commit(repository: str, tag: str) -> str | None:
    ref = optional_api(f"repos/{repository}/git/ref/tags/{tag}")
    if ref is None:
        return None
    obj = ref["object"]
    # Annotated tags point to tag objects, not directly to commits.
    for _ in range(10):
        sha = obj["sha"]
        if not isinstance(sha, str) or re.fullmatch(r"[0-9a-f]{40}", sha) is None:
            raise PublishError("Invalid tag object SHA")
        if obj["type"] == "commit":
            return sha
        if obj["type"] != "tag":
            break
        obj = api(f"repos/{repository}/git/tags/{sha}")["object"]
    raise PublishError("Tag does not resolve to a commit")


def expected_files(version: str) -> set[str]:
    return {
        name
        for package in ("modelctl", "modelctl_core", "modelctl_sdk")
        for name in (f"{package}-{version}-py3-none-any.whl", f"{package}-{version}.tar.gz")
    }


def verify_bundle(directory: Path, version: str, *, allow_build_metadata: bool = False) -> None:
    expected = expected_files(version)
    names = {path.name for path in directory.iterdir()}
    if allow_build_metadata:
        names.discard(".gitignore")  # uv build creates this local-only marker.
    if names != expected | {"SHA256SUMS"}:
        raise PublishError("Release must contain exactly six distributions and SHA256SUMS")
    hashes = {}
    for line in (directory / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64}) [ *](?:dist/)?([^/\\]+)", line)
        if match is None or match[2] not in expected or match[2] in hashes:
            raise PublishError("Invalid or duplicate checksum entry")
        hashes[match[2]] = match[1]
    if set(hashes) != expected:
        raise PublishError("Checksums do not cover all six distributions")
    for name, digest in hashes.items():
        path = directory / name
        if path.is_symlink() or not path.is_file():
            raise PublishError(f"Invalid release file: {name}")
        if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise PublishError(f"Checksum mismatch: {name}")


def require_target(repository: str, tag: str, target: str) -> None:
    actual = tag_commit(repository, tag)
    if actual != target:
        raise PublishError(f"{tag} points to {actual}, expected {target}; refusing to move it")


def verify_remote(repository: str, tag: str, version: str, release: dict) -> None:
    names = [asset["name"] for asset in release["assets"]]
    if len(names) != 7 or set(names) != expected_files(version) | {"SHA256SUMS"}:
        raise PublishError("Existing release is incomplete; no overwrite or automatic repair")
    with tempfile.TemporaryDirectory(prefix="modelctl-release-") as temporary:
        result = gh("release", "download", tag, "--repo", repository, "--dir", temporary)
        if result.returncode:
            raise PublishError("Could not download release assets for verification")
        # Rebuilds can differ byte-for-byte: verify the published bundle against
        # its own immutable checksum manifest, not a later rebuild's manifest.
        verify_bundle(Path(temporary), version)


def publish(repository: str, tag: str, target: str, auto_create: bool, dist: Path) -> None:
    if re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository) is None:
        raise PublishError("Invalid repository")
    tag_pattern = r"v[0-9]+\.[0-9]+\.[0-9]+(?:(?:a|b|rc)[0-9]+|\.post[0-9]+|\.dev[0-9]+)?"
    if re.fullmatch(tag_pattern, tag) is None:
        raise PublishError("Invalid release tag")
    if re.fullmatch(r"[0-9a-f]{40}", target) is None:
        raise PublishError("Invalid target commit")
    version = tag[1:]
    verify_bundle(dist, version, allow_build_metadata=True)
    actual = tag_commit(repository, tag)
    if actual is None:
        if not auto_create:
            raise PublishError("Manually triggered tag no longer exists")
        try:
            api(f"repos/{repository}/git/refs", method="POST", fields=(
                "-f", f"ref=refs/tags/{tag}", "-f", f"sha={target}",
            ))
        except APIError as error:
            if error.status not in (409, 422):
                raise
            # Another publisher may have created it after the lookup.
    require_target(repository, tag, target)

    endpoint = f"repos/{repository}/releases/tags/{tag}"
    release = find_release(repository, tag)
    if release is None:
        result = gh(
            "release", "create", tag,
            *[str(dist / name) for name in sorted(expected_files(version) | {"SHA256SUMS"})],
            "--repo", repository, "--verify-tag", "--generate-notes", "--title", tag,
            "--draft",
        )
        if result.returncode:
            # Do not blindly retry uploads: a partial draft must remain private.
            raise PublishError("Release creation failed; inspect any draft before retrying")
        release = find_release(repository, tag)
        if release is None:
            raise PublishError("Created draft could not be found")
    verify_remote(repository, tag, version, release)
    require_target(repository, tag, target)
    if release["draft"]:
        result = gh("release", "edit", tag, "--repo", repository, "--draft=false")
        if result.returncode:
            raise PublishError("Could not publish verified draft")
    final = api(endpoint)
    if final["draft"]:
        raise PublishError("Release is still a draft")
    verify_remote(repository, tag, version, final)
    require_target(repository, tag, target)
    print(f"Verified {tag} at {target}: six distributions and SHA256SUMS; no overwrite.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-bundle", action="store_true", help="Validate dist without GitHub")
    args = parser.parse_args()
    try:
        if args.verify_bundle:
            manifest = tomllib.loads(Path("release.toml").read_text(encoding="utf-8"))
            verify_bundle(Path("dist"), manifest["version"], allow_build_metadata=True)
            print("Verified local bundle: six distributions and SHA256SUMS")
            return 0
        publish(
            os.environ["REPOSITORY"], os.environ["RELEASE_TAG"], os.environ["TARGET_SHA"],
            os.environ["AUTO_CREATE_TAG"] == "true", Path("dist"),
        )
    except (PublishError, OSError, KeyError, TypeError, ValueError) as error:
        print(f"Release publication failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
