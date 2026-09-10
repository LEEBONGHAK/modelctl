"""Exercise the real publisher with a stateful, network-free gh transport."""

import hashlib
import json
import shutil
import subprocess
import sys
from importlib import import_module
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
publisher = import_module("scripts.publish_release")


TARGET = "a" * 40
OTHER = "b" * 40
ANNOTATED = "c" * 40
REPOSITORY = "owner/modelctl"
TAG = "v0.3.0"


def bundle(directory: Path):
    directory.mkdir()
    lines = []
    for name in sorted(publisher.expected_files("0.3.0")):
        data = name.encode()
        (directory / name).write_bytes(data)
        lines.append(f"{hashlib.sha256(data).hexdigest()}  dist/{name}\n")
    (directory / "SHA256SUMS").write_text("".join(lines), encoding="utf-8")


class FakeGitHub:
    def __init__(self, dist):
        self.dist = dist
        self.tag = None
        self.release = None
        self.calls = []
        self.lookup_error = None
        self.release_error = None
        self.race = None
        self.create_error = None
        self.partial_upload = False
        self.corrupt_download = False
        self.malformed = False

    def run(self, command, **kwargs):
        assert command[0] == "gh"
        assert kwargs == {"capture_output": True, "text": True, "check": False}
        args = command[1:]
        self.calls.append(args)

        def response(status, body):
            stdout = f"HTTP/2.0 {status} Status\nContent-Type: application/json\n\n"
            stdout += json.dumps(body)
            return subprocess.CompletedProcess(command, int(status >= 400), stdout, "")

        if args[0] == "api":
            assert args[1:3] == ["--include", "--method"]
            method, endpoint = args[3:5]
            assert endpoint.startswith(f"repos/{REPOSITORY}/")
            if "/git/ref/tags/" in endpoint:
                if self.malformed:
                    return subprocess.CompletedProcess(command, 1, "not HTTP", "network failure")
                if self.lookup_error:
                    return response(self.lookup_error, {"message": "failure"})
                if self.tag is None:
                    return response(404, {"message": "Not Found"})
                kind = "tag" if self.tag == ANNOTATED else "commit"
                return response(200, {"object": {"type": kind, "sha": self.tag}})
            if "/git/tags/" in endpoint:
                return response(200, {"object": {"type": "commit", "sha": TARGET}})
            if endpoint.endswith("/git/refs"):
                assert method == "POST"
                assert args[5:] == ["-f", f"ref=refs/tags/{TAG}", "-f", f"sha={TARGET}"]
                if self.create_error:
                    return response(self.create_error, {"message": "failure"})
                if self.race:
                    self.tag = self.race
                    return response(422, {"message": "Reference already exists"})
                self.tag = TARGET
                return response(201, {"object": {"type": "commit", "sha": TARGET}})
            if "/releases/tags/" in endpoint:
                if self.release_error:
                    return response(self.release_error, {"message": "failure"})
                if self.release and not self.release["draft"]:
                    return response(200, self.release)
                return response(404, {})
            if "/releases?" in endpoint:
                return response(200, [self.release] if self.release else [])
            raise AssertionError(args)

        assert "--repo" in args
        assert args[args.index("--repo") + 1] == REPOSITORY
        if args[:2] == ["release", "create"]:
            assert "--draft" in args and "--verify-tag" in args
            assert not any(arg.endswith(".gitignore") for arg in args)
            self.release = self.complete_release(draft=True)
            if self.partial_upload:
                self.release["assets"].pop()
                return subprocess.CompletedProcess(command, 1, "", "upload failed")
        elif args[:2] == ["release", "download"]:
            destination = Path(args[args.index("--dir") + 1])
            for asset in self.release["assets"]:
                shutil.copyfile(self.dist / asset["name"], destination / asset["name"])
            if self.corrupt_download:
                (destination / sorted(publisher.expected_files("0.3.0"))[0]).write_bytes(b"bad")
        elif args[:2] == ["release", "edit"]:
            assert "--draft=false" in args
            self.release["draft"] = False
        else:
            raise AssertionError(args)
        return subprocess.CompletedProcess(command, 0, "", "")

    def complete_release(self, draft=False):
        return {
            "tag_name": TAG, "draft": draft,
            "assets": [{"name": p.name} for p in self.dist.iterdir() if p.name != ".gitignore"],
        }

    def writes(self):
        return [args for args in self.calls if "POST" in args or args[:2] in (
            ["release", "create"], ["release", "edit"],
        )]


@pytest.fixture
def github(tmp_path, monkeypatch):
    dist = tmp_path / "dist"
    bundle(dist)
    fake = FakeGitHub(dist)
    monkeypatch.setattr(publisher.subprocess, "run", fake.run)
    return fake


def publish(github, auto_create=True):
    publisher.publish(REPOSITORY, TAG, TARGET, auto_create, github.dist)


def test_first_release_is_verified_before_draft_becomes_public(github):
    publish(github)
    assert github.tag == TARGET
    assert github.release["draft"] is False
    operations = [args[:2] for args in github.calls]
    assert operations.index(["release", "download"]) < operations.index(["release", "edit"])
    assert operations.count(["release", "download"]) == 2


def test_uv_build_metadata_is_not_uploaded(github):
    (github.dist / ".gitignore").write_text("*")
    publish(github)
    assert len(github.release["assets"]) == 7


@pytest.mark.parametrize("status", [401, 403, 429, 500, 503])
def test_non_404_tag_lookup_errors_never_write(github, status):
    github.lookup_error = status
    with pytest.raises(publisher.APIError):
        publish(github)
    assert github.writes() == []


def test_network_failure_never_writes(github):
    github.malformed = True
    with pytest.raises(publisher.PublishError, match="HTTP response"):
        publish(github)
    assert github.writes() == []


@pytest.mark.parametrize("status", [403, 500])
def test_non_404_release_lookup_error_does_not_create_release(github, status):
    github.tag = TARGET
    github.release_error = status
    with pytest.raises(publisher.APIError):
        publish(github)
    assert github.writes() == []


def test_concurrent_tag_creation_rechecks_same_commit(github):
    github.race = TARGET
    publish(github)
    assert github.release["draft"] is False


def test_concurrent_tag_creation_at_other_commit_fails(github):
    github.race = OTHER
    with pytest.raises(publisher.PublishError, match="refusing to move"):
        publish(github)
    assert github.release is None
    assert github.tag == OTHER


@pytest.mark.parametrize("status", [403, 422, 500])
def test_failed_tag_creation_cannot_publish(github, status):
    github.create_error = status
    with pytest.raises(publisher.PublishError):
        publish(github)
    assert github.release is None


def test_conflicting_existing_tag_fails_without_writes(github):
    github.tag = OTHER
    with pytest.raises(publisher.PublishError, match="refusing to move"):
        publish(github)
    assert github.writes() == []


@pytest.mark.parametrize("tag", [TARGET, ANNOTATED])
def test_tag_only_retry_and_annotated_tag(github, tag):
    github.tag = tag
    publish(github)
    assert not any("POST" in args for args in github.calls)
    assert github.release["draft"] is False


def test_completed_release_retry_verifies_without_writes(github):
    github.tag = TARGET
    github.release = github.complete_release()
    publish(github)
    assert github.writes() == []


def test_complete_draft_retry_verifies_then_publishes(github):
    github.tag = TARGET
    github.release = github.complete_release(draft=True)
    publish(github)
    assert len(github.writes()) == 1
    assert github.writes()[0][:2] == ["release", "edit"]


@pytest.mark.parametrize("draft", [True, False])
def test_incomplete_existing_release_fails_without_replacing_assets(github, draft):
    github.tag = TARGET
    github.release = github.complete_release(draft=draft)
    github.release["assets"].pop()
    with pytest.raises(publisher.PublishError, match="incomplete"):
        publish(github)
    assert github.writes() == []


def test_interrupted_upload_stays_private(github):
    github.partial_upload = True
    with pytest.raises(publisher.PublishError, match="creation failed"):
        publish(github)
    assert github.release["draft"] is True


def test_corrupt_uploaded_bytes_prevent_publication(github):
    github.corrupt_download = True
    with pytest.raises(publisher.PublishError, match="Checksum mismatch"):
        publish(github)
    assert github.release["draft"] is True


def test_missing_manual_tag_cannot_be_recreated(github):
    with pytest.raises(publisher.PublishError, match="no longer exists"):
        publish(github, auto_create=False)
    assert github.writes() == []


@pytest.mark.parametrize("problem", ["missing", "corrupt", "duplicate", "traversal"])
def test_bad_local_bundle_fails_before_any_api_call(github, problem):
    name = sorted(publisher.expected_files("0.3.0"))[0]
    checksums = github.dist / "SHA256SUMS"
    if problem == "missing":
        (github.dist / name).unlink()
    elif problem == "corrupt":
        (github.dist / name).write_bytes(b"bad")
    elif problem == "duplicate":
        checksums.write_text(checksums.read_text() * 2)
    else:
        checksums.write_text(checksums.read_text().replace("dist/", "../"))
    with pytest.raises(publisher.PublishError):
        publish(github)
    assert github.calls == []
