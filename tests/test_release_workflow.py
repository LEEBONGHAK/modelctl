from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "release.yml"


def workflow_text() -> str:
    return WORKFLOW.read_text(encoding="utf-8")


def test_release_workflow_runs_all_quality_gates_before_publication():
    content = workflow_text()

    required_commands = (
        "uv sync --all-packages --locked",
        "uv audit --locked",
        "uv run ruff check .",
        "uv run basedpyright",
        "uv run pytest",
        "uv build packages/core --out-dir dist --no-sources",
        "uv build packages/sdk --out-dir dist --no-sources",
        "uv build apps/modelctl --out-dir dist --no-sources",
        'files("modelctl_core").joinpath("py.typed").is_file()',
        'files("modelctl_sdk").joinpath("py.typed").is_file()',
        ".release-smoke/bin/modelctl version",
        ".release-smoke/bin/modelctl --help",
        "sha256sum dist/* > dist/SHA256SUMS",
        "python scripts/publish_release.py --verify-bundle",
    )

    for command in required_commands:
        assert command in content


def test_release_workflow_tracks_type_check_configuration_changes():
    content = workflow_text()

    assert content.count('- "pyproject.toml"') >= 2


def test_release_workflow_only_auto_tags_trusted_ready_main_changes():
    content = workflow_text()

    assert "github.ref == 'refs/heads/main'" in content
    assert "github.event.action == 'closed'" in content
    assert "github.event.pull_request.merged == true" in content
    assert "github.event.pull_request.base.ref == 'main'" in content
    assert "github.event.pull_request.merge_commit_sha" in content
    assert "needs.validate-and-build.outputs.status == 'ready'" in content
    assert "AUTO_CREATE_TAG" in content
    assert "git fetch origin main" in content
    assert "python scripts/publish_release.py" in content


def test_both_publishers_share_serialization_and_implementation():
    for name in ("release.yml", "release-command.yml"):
        content = (ROOT / ".github/workflows" / name).read_text(encoding="utf-8")
        publisher = content.split("  publish-release:", 1)[1]
        assert "group: modelctl-publish-${{ needs.validate-and-build.outputs.tag }}" in publisher
        assert "cancel-in-progress: false" in publisher
        assert "python scripts/publish_release.py" in publisher
        assert "persist-credentials: false" in publisher
        assert "gh release create" not in publisher


def test_release_workflow_tracks_publisher_and_behavior_tests():
    content = workflow_text()
    assert content.count('- "scripts/publish_release.py"') == 2
    assert content.count('- "tests/test_publish_release.py"') == 2


def test_release_workflow_skips_closed_unmerged_pull_requests():
    content = workflow_text()

    assert "github.event.action != 'closed'" in content
    assert "github.event.pull_request.merged == true" in content


def test_release_workflow_keeps_pypi_disabled():
    content = workflow_text()

    assert "uv publish" not in content
    assert "publish-pypi" not in content
    assert "id-token: write" not in content
