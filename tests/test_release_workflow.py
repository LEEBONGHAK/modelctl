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
        "uv run pytest",
        "uv build packages/core --out-dir dist --no-sources",
        "uv build packages/sdk --out-dir dist --no-sources",
        "uv build apps/modelctl --out-dir dist --no-sources",
        ".release-smoke/bin/modelctl version",
        ".release-smoke/bin/modelctl --help",
        "sha256sum dist/* > dist/SHA256SUMS",
    )

    for command in required_commands:
        assert command in content


def test_release_workflow_only_auto_tags_trusted_ready_refac_changes():
    content = workflow_text()

    assert "github.ref == 'refs/heads/refac'" in content
    assert "github.event.action == 'closed'" in content
    assert "github.event.pull_request.merged == true" in content
    assert "github.event.pull_request.base.ref == 'refac'" in content
    assert "github.event.pull_request.merge_commit_sha" in content
    assert "needs.validate-and-build.outputs.status == 'ready'" in content
    assert "AUTO_CREATE_TAG" in content
    assert 'ref="refs/tags/${RELEASE_TAG}"' in content
    assert 'sha="${TARGET_SHA}"' in content
    assert "already points" in content
    assert "no overwrite" in content


def test_release_workflow_skips_closed_unmerged_pull_requests():
    content = workflow_text()

    assert "github.event.action != 'closed'" in content
    assert "github.event.pull_request.merged == true" in content


def test_release_workflow_keeps_pypi_disabled():
    content = workflow_text()

    assert "uv publish" not in content
    assert "publish-pypi" not in content
    assert "id-token: write" not in content
