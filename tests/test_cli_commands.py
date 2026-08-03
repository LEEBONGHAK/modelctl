from typer.testing import CliRunner

from modelctl_cli.main import app


runner = CliRunner()


def test_use_and_run_are_top_level_commands():
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "use" in result.stdout
    assert "run" in result.stdout


def test_nested_use_command_is_not_required():
    result = runner.invoke(app, ["use", "--help"])

    assert result.exit_code == 0
    assert "Select and persist the default provider and model." in result.stdout


def test_nested_run_command_is_not_required():
    result = runner.invoke(app, ["run", "--help"])

    assert result.exit_code == 0
    assert "Launch the configured coding agent" in result.stdout
