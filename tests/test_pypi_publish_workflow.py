from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "publish-pypi.yml"


def workflow_text() -> str:
    return WORKFLOW.read_text(encoding="utf-8")


def test_pypi_workflow_is_manual_and_locked_to_v010():
    content = workflow_text()

    assert "workflow_dispatch:" in content
    assert "inputs.tag == 'v0.1.0'" in content
    assert "inputs.confirmation == 'publish-v0.1.0'" in content
    assert "ref: ${{ inputs.tag }}" in content
    assert 'test "$(git describe --tags --exact-match)" = "v0.1.0"' in content
    assert "python scripts/release_validation.py --tag v0.1.0" in content


def test_pypi_workflow_revalidates_before_upload():
    content = workflow_text()

    required_commands = (
        "uv sync --all-packages --locked",
        "uv audit --locked",
        "uv run ruff check .",
        "uv run pytest",
        "uv build packages/core --out-dir dist --no-sources",
        "uv build packages/sdk --out-dir dist --no-sources",
        "uv build apps/modelctl --out-dir dist --no-sources",
        "uvx twine check dist/*",
    )

    for command in required_commands:
        assert command in content


def test_pypi_workflow_requires_protected_environment_and_secret():
    content = workflow_text()

    assert "environment:" in content
    assert "name: pypi" in content
    assert "secrets.PYPI_API_TOKEN" in content
    assert "pypa/gh-action-pypi-publish@" in content
    assert "skip-existing: false" in content
