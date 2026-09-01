from types import SimpleNamespace
from unittest.mock import Mock, patch

from typer.testing import CliRunner

from modelctl_cli.main import app

runner = CliRunner()


def test_launchers_list_shows_plugin_source_and_broken_entry_point():
    plugin_launcher = SimpleNamespace(
        name="custom",
        display_name="Custom Launcher",
        available=lambda: True,
    )
    loaded = SimpleNamespace(
        launcher_id="custom",
        display_name="Custom Launcher",
        plugin_id="example.plugin",
        source="modelctl-custom==1.0.0",
        status="loaded",
        error=None,
    )
    broken = SimpleNamespace(
        launcher_id="broken",
        display_name=None,
        plugin_id=None,
        source="broken-plugin==1.0.0",
        status="error",
        error="ImportError: boom",
    )

    fake_container = Mock()
    fake_container.config.load.return_value = {"launcher": "custom"}
    fake_container.launchers.list.return_value = [plugin_launcher]
    fake_container.launchers.diagnostics.return_value = [loaded, broken]

    with patch("modelctl_cli.commands.launchers.container", fake_container):
        result = runner.invoke(app, ["launchers", "list"])

    assert result.exit_code == 0
    assert "custom" in result.stdout
    assert "loaded" in result.stdout
    assert "broken" in result.stdout
    assert "error" in result.stdout
    assert "ImportError" in result.stdout
