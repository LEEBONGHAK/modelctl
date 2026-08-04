from types import SimpleNamespace
from unittest.mock import Mock, patch

from typer.testing import CliRunner

from modelctl_cli.main import app

runner = CliRunner()


def launcher(name: str, display_name: str, installed: bool):
    return SimpleNamespace(
        name=name,
        display_name=display_name,
        available=lambda: installed,
    )


def recommendation(active: bool = False, changed: bool = False):
    return SimpleNamespace(
        name="aider",
        display_name="Aider",
        provider="openrouter",
        model="anthropic/claude-sonnet-4",
        reason="Aider translates OpenRouter model identifiers automatically.",
        installed=True,
        active=active,
        changed=changed,
    )


def test_launchers_list_shows_supported_and_active_launchers():
    claude = launcher("claude", "Claude Code", True)
    aider = launcher("aider", "Aider", False)
    fake_container = Mock()
    fake_container.config.load.return_value = {"launcher": "aider"}
    fake_container.launchers.list.return_value = [claude, aider]

    with patch("modelctl_cli.commands.launchers.container", fake_container):
        result = runner.invoke(app, ["launchers", "list"])

    assert result.exit_code == 0
    assert "Claude Code" in result.stdout
    assert "Aider" in result.stdout
    assert "Installed" in result.stdout


def test_launchers_recommend_shows_provider_aware_choice():
    service = Mock()
    service.recommend.return_value = recommendation()
    fake_container = Mock()
    fake_container.launcher_service.return_value = service

    with patch("modelctl_cli.commands.launchers.container", fake_container):
        result = runner.invoke(app, ["launchers", "recommend"])

    assert result.exit_code == 0
    assert "Launcher recommendation" in result.stdout
    assert "openrouter" in result.stdout
    assert "anthropic/claude-sonnet-4" in result.stdout
    assert "Aider" in result.stdout
    assert "translates OpenRouter" in result.stdout
    service.recommend.assert_called_once_with()


def test_launchers_recommend_apply_reports_selected_launcher():
    service = Mock()
    service.apply_recommendation.return_value = recommendation(active=True, changed=True)
    fake_container = Mock()
    fake_container.launcher_service.return_value = service

    with patch("modelctl_cli.commands.launchers.container", fake_container):
        result = runner.invoke(app, ["launchers", "recommend", "--apply"])

    assert result.exit_code == 0
    assert "Selected recommended launcher" in result.stdout
    assert "already selected" not in result.stdout
    service.apply_recommendation.assert_called_once_with()


def test_launchers_recommend_apply_reports_already_active_launcher():
    service = Mock()
    service.apply_recommendation.return_value = recommendation(active=True)
    fake_container = Mock()
    fake_container.launcher_service.return_value = service

    with patch("modelctl_cli.commands.launchers.container", fake_container):
        result = runner.invoke(app, ["launchers", "recommend", "--apply"])

    assert result.exit_code == 0
    assert "already selected" in result.stdout
    assert "Selected recommended launcher" not in result.stdout


def test_launchers_recommend_reports_missing_recommendation():
    service = Mock()
    service.recommend.return_value = None
    fake_container = Mock()
    fake_container.launcher_service.return_value = service
    fake_container.config.load.return_value = {"provider": "custom"}

    with patch("modelctl_cli.commands.launchers.container", fake_container):
        result = runner.invoke(app, ["launchers", "recommend"])

    assert result.exit_code == 1
    assert "No launcher recommendation" in result.stdout
    assert "custom" in result.stdout


def test_launchers_use_persists_selected_launcher():
    codex = launcher("codex", "Codex CLI", True)
    fake_container = Mock()
    fake_container.launchers.get.return_value = codex

    with patch("modelctl_cli.commands.launchers.container", fake_container):
        result = runner.invoke(app, ["launchers", "use", "codex"])

    assert result.exit_code == 0
    assert "Selected launcher" in result.stdout
    fake_container.config.update.assert_called_once_with(launcher="codex")


def test_launchers_use_rejects_unknown_launcher():
    fake_container = Mock()
    fake_container.launchers.get.return_value = None
    fake_container.launchers.list.return_value = [
        launcher("claude", "Claude Code", True),
        launcher("gemini", "Gemini CLI", True),
    ]

    with patch("modelctl_cli.commands.launchers.container", fake_container):
        result = runner.invoke(app, ["launchers", "use", "unknown"])

    assert result.exit_code != 0
    assert "Unknown launcher 'unknown'" in result.output
