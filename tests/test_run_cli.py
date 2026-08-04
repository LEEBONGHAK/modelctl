from unittest.mock import Mock, patch

from typer.testing import CliRunner

from modelctl_cli.main import app

runner = CliRunner()


def test_run_forwards_unknown_native_options_to_launcher():
    service = Mock()
    service.check_compatibility.return_value = None
    fake_container = Mock()
    fake_container.launcher_service.return_value = service

    with patch("modelctl_cli.commands.run.container", fake_container):
        result = runner.invoke(app, ["run", "--continue", "--verbose"])

    assert result.exit_code == 0
    service.check_compatibility.assert_called_once_with(policy=None)
    service.run.assert_called_once_with(["--continue", "--verbose"])


def test_run_uses_persisted_compatibility_policy_without_override():
    service = Mock()
    service.check_compatibility.return_value = "Potential mismatch"
    fake_container = Mock()
    fake_container.launcher_service.return_value = service

    with patch("modelctl_cli.commands.run.container", fake_container):
        result = runner.invoke(app, ["run"])

    assert result.exit_code == 0
    assert "Compatibility warning" in result.stdout
    service.check_compatibility.assert_called_once_with(policy=None)
    service.run.assert_called_once_with([])


def test_run_strict_compatibility_blocks_mismatch():
    service = Mock()
    service.check_compatibility.side_effect = RuntimeError(
        "Strict compatibility check failed: Potential mismatch"
    )
    fake_container = Mock()
    fake_container.launcher_service.return_value = service

    with patch("modelctl_cli.commands.run.container", fake_container):
        result = runner.invoke(app, ["run", "--strict-compatibility"])

    assert result.exit_code == 1
    assert "Strict compatibility check failed" in result.stdout
    service.check_compatibility.assert_called_once_with(policy="strict")
    service.run.assert_not_called()


def test_run_warn_compatibility_overrides_persisted_strict_policy():
    service = Mock()
    service.check_compatibility.return_value = "Potential mismatch"
    fake_container = Mock()
    fake_container.launcher_service.return_value = service

    with patch("modelctl_cli.commands.run.container", fake_container):
        result = runner.invoke(app, ["run", "--warn-compatibility"])

    assert result.exit_code == 0
    assert "Compatibility warning" in result.stdout
    service.check_compatibility.assert_called_once_with(policy="warn")
    service.run.assert_called_once_with([])


def test_run_strict_compatibility_preserves_launcher_arguments():
    service = Mock()
    service.check_compatibility.return_value = None
    fake_container = Mock()
    fake_container.launcher_service.return_value = service

    with patch("modelctl_cli.commands.run.container", fake_container):
        result = runner.invoke(
            app,
            ["run", "--strict-compatibility", "--sandbox", "workspace-write"],
        )

    assert result.exit_code == 0
    service.check_compatibility.assert_called_once_with(policy="strict")
    service.run.assert_called_once_with(["--sandbox", "workspace-write"])
