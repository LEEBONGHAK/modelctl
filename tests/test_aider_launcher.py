from unittest.mock import patch

from modelctl_core.launcher.aider import AiderLauncher
from modelctl_core.launcher.base import LaunchRequest
from modelctl_core.launcher.registry import LauncherRegistry


def test_aider_prefixes_openrouter_model():
    launcher = AiderLauncher()
    request = LaunchRequest.create(
        "anthropic/claude-sonnet-4",
        provider="openrouter",
        extra_args=["--no-auto-commits"],
    )

    with (
        patch.object(launcher, "available", return_value=True),
        patch("modelctl_core.launcher.aider.subprocess.run") as run,
    ):
        launcher.run(request)

    run.assert_called_once_with(
        [
            "aider",
            "--model",
            "openrouter/anthropic/claude-sonnet-4",
            "--no-auto-commits",
        ],
        check=True,
    )


def test_aider_preserves_non_openrouter_model():
    assert AiderLauncher._model_name("gpt-5.6", "openai") == "gpt-5.6"


def test_aider_does_not_duplicate_openrouter_prefix():
    model = "openrouter/anthropic/claude-sonnet-4"

    assert AiderLauncher._model_name(model, "openrouter") == model


def test_aider_reports_missing_cli():
    launcher = AiderLauncher()

    with patch.object(launcher, "available", return_value=False):
        try:
            launcher.run(LaunchRequest.create("gpt-5.6"))
        except RuntimeError as exc:
            assert "aider-install" in str(exc)
        else:
            raise AssertionError("Expected RuntimeError")


def test_aider_launcher_is_registered():
    launcher = LauncherRegistry().get("aider")

    assert isinstance(launcher, AiderLauncher)
    assert launcher.capabilities.accepts_any_provider is True
    assert launcher.capabilities.translates("openrouter") is True
