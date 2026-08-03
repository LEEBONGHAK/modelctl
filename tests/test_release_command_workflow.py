from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "release-command.yml"


def workflow_text() -> str:
    return WORKFLOW.read_text(encoding="utf-8")


def test_release_command_requires_owner_and_merged_main_pull_request():
    content = workflow_text()

    assert "issue_comment:" in content
    assert "github.event.comment.author_association == 'OWNER'" in content
    assert "startsWith(github.event.comment.body, '/release ')" in content
    assert ".merged_at // empty" in content
    assert '"${base_ref}" != "main"' in content
    assert ".merge_commit_sha // empty" in content
    assert "git merge-base --is-ancestor" in content
    assert "origin/main" in content


def test_release_command_validates_before_exporting_or_publishing():
    content = workflow_text()

    validation = "python scripts/release_validation.py --tag \"${tag}\""
    output = "printf 'tag=%s\\n' \"${tag}\" >> \"${GITHUB_OUTPUT}\""
    assert validation in content
    assert output in content
    assert content.index(validation) < content.index(output)
    assert "RELEASE_STATUS" in content
    assert '"${RELEASE_STATUS}" != "ready"' in content


def test_release_command_runs_complete_release_gates():
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


def test_release_command_keeps_tag_release_and_pypi_immutable():
    content = workflow_text()

    assert "refusing to move it" in content
    assert "already exists; no overwrite" in content
    assert "uv publish" not in content
    assert "publish-pypi" not in content
    assert "id-token: write" not in content
