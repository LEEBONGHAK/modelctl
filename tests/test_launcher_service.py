from unittest.mock import Mock

from modelctl_core.services.launcher_service import LauncherService


def test_launcher_service_forwards_provider_context():
    launcher = Mock()
    registry = Mock()
    registry.get.return_value = launcher
    config = Mock()
    config.load.return_value = {
        "launcher": "aider",
        "provider": "openrouter",
        "default_model": "anthropic/claude-sonnet-4",
    }

    LauncherService(registry, config).run(["--no-auto-commits"])

    registry.get.assert_called_once_with("aider")
    launcher.run.assert_called_once_with(
        "anthropic/claude-sonnet-4",
        ["--no-auto-commits"],
        provider="openrouter",
    )
