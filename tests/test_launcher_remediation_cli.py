from types import SimpleNamespace
from unittest.mock import Mock, patch

from typer.testing import CliRunner

from modelctl_cli.main import app

runner = CliRunner()


def remediation(
    *,
    action_required: bool = True,
    installed: bool = True,
    changed: bool = False,
):
    return SimpleNamespace(
        provider="openrouter",
        model="anthropic/claude-sonnet-4",
        current_name="claude",
        current_display_name="Claude Code",
        warning="Potential mismatch" if action_required else None,
        recommended_name="aider" if action_required else "claude",
        recommended_display_name="Aider" if action_required else "Claude Code",
        recommended_installed=installed,
        reason=(
            "Aider translates openrouter model identifiers automatically."
            if action_required
            else "No known compatibility issue requires remediation."
        ),
        action_required=action_required,
        changed=changed,
    )


def test_launchers_remediate_previews_plan_without_applying():
    service = Mock()
    service.plan_remediation.return_value = remediation()
    fake_container = Mock()
    fake_container.launcher_service.return_value = service

    with patch("modelctl_cli.commands.launchers.container", fake_container):
        result = runner.invoke(app, ["launchers", "remediate"])

    assert result.exit_code == 0
    assert "Compatibility remediation plan" in result.stdout
    assert "Claude Code" in result.stdout
    assert "Aider" in result.stdout
    assert "Potential mismatch" in result.stdout
    assert "Preview only" in result.stdout
    service.plan_remediation.assert_called_once_with()
    service.apply_remediation.assert_not_called()


def test_launchers_remediate_apply_reports_configuration_change():
    service = Mock()
    service.apply_remediation.return_value = remediation(changed=True)
    fake_container = Mock()
    fake_container.launcher_service.return_value = service

    with patch("modelctl_cli.commands.launchers.container", fake_container):
        result = runner.invoke(app, ["launchers", "remediate", "--apply"])

    assert result.exit_code == 0
    assert "Applied compatibility remediation" in result.stdout
    service.apply_remediation.assert_called_once_with()
    service.plan_remediation.assert_not_called()


def test_launchers_remediate_reports_no_required_change():
    service = Mock()
    service.plan_remediation.return_value = remediation(action_required=False)
    fake_container = Mock()
    fake_container.launcher_service.return_value = service

    with patch("modelctl_cli.commands.launchers.container", fake_container):
        result = runner.invoke(app, ["launchers", "remediate"])

    assert result.exit_code == 0
    assert "No compatibility remediation is required" in result.stdout


def test_launchers_remediate_previews_unavailable_recommendation():
    service = Mock()
    service.plan_remediation.return_value = remediation(installed=False)
    fake_container = Mock()
    fake_container.launcher_service.return_value = service

    with patch("modelctl_cli.commands.launchers.container", fake_container):
        result = runner.invoke(app, ["launchers", "remediate"])

    assert result.exit_code == 0
    assert "Install the recommended launcher" in result.stdout


def test_launchers_remediate_reports_service_failure():
    service = Mock()
    service.plan_remediation.side_effect = RuntimeError(
        "No automatic compatibility remediation is available"
    )
    fake_container = Mock()
    fake_container.launcher_service.return_value = service

    with patch("modelctl_cli.commands.launchers.container", fake_container):
        result = runner.invoke(app, ["launchers", "remediate"])

    assert result.exit_code == 1
    assert "Compatibility remediation failed" in result.stdout
    assert "No automatic compatibility remediation" in result.stdout
