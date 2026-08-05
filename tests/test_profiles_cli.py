import re
from types import SimpleNamespace
from unittest.mock import Mock, patch

from typer.testing import CliRunner

from modelctl_cli.commands.profiles import profiles_app

runner = CliRunner()
ANSI_ESCAPE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")


def profile(name: str = "work"):
    return SimpleNamespace(
        name=name,
        provider="openrouter",
        model="anthropic/claude-sonnet-4",
        launcher="aider",
        compatibility_policy="strict",
    )


def invoke(arguments: list[str], service: Mock):
    fake_container = Mock()
    fake_container.profile_service.return_value = service
    with patch("modelctl_cli.commands.profiles.container", fake_container):
        return runner.invoke(profiles_app, arguments)


def test_profiles_save_reports_normalized_name():
    service = Mock()
    service.save.return_value = profile()

    result = invoke(["save", "WORK"], service)

    assert result.exit_code == 0
    assert "Saved profile" in result.stdout
    assert "work" in result.stdout
    service.save.assert_called_once_with("WORK")


def test_profiles_list_shows_saved_snapshots():
    service = Mock()
    service.list.return_value = [profile()]

    result = invoke(["list"], service)

    assert result.exit_code == 0
    assert "Named profiles" in result.stdout
    assert "openrouter" in result.stdout
    assert "anthropic/claude-sonnet-4" in result.stdout
    assert "aider" in result.stdout
    assert "strict" in result.stdout


def test_profiles_list_reports_empty_state():
    service = Mock()
    service.list.return_value = []

    result = invoke(["list"], service)

    assert result.exit_code == 0
    assert "No saved profiles" in result.stdout


def test_profiles_show_use_and_delete_delegate_to_service():
    service = Mock()
    service.get.return_value = profile()
    service.use.return_value = profile()
    service.delete.return_value = profile()

    shown = invoke(["show", "work"], service)
    used = invoke(["use", "work"], service)
    deleted = invoke(["delete", "work"], service)

    assert shown.exit_code == used.exit_code == deleted.exit_code == 0
    assert "Profile: work" in shown.stdout
    assert "Applied profile" in used.stdout
    assert "Deleted profile" in deleted.stdout
    service.get.assert_called_once_with("work")
    service.use.assert_called_once_with("work")
    service.delete.assert_called_once_with("work")


def test_profiles_reports_validation_errors_as_cli_errors():
    service = Mock()
    service.use.side_effect = ValueError("Unknown profile: missing")

    result = invoke(["use", "missing"], service)

    output = " ".join(ANSI_ESCAPE.sub("", result.output).split())
    assert result.exit_code != 0
    assert "Unknown profile: missing" in output
