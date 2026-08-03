from typer.testing import CliRunner

from modelctl_cli.commands import root
from modelctl_cli.main import app


runner = CliRunner()


def test_version_command_reads_installed_distribution_metadata(monkeypatch):
    monkeypatch.setattr(root.metadata, "version", lambda package: "9.8.7")

    result = runner.invoke(app, ["version"])

    assert result.exit_code == 0
    assert result.stdout.strip() == "modelctl 9.8.7"


def test_installed_version_handles_source_tree_without_distribution(monkeypatch):
    def missing_distribution(package):
        raise root.metadata.PackageNotFoundError(package)

    monkeypatch.setattr(root.metadata, "version", missing_distribution)

    assert root.installed_version() == "unknown"
