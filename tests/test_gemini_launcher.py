from unittest.mock import patch

from modelctl_core.launcher.gemini import GeminiCliLauncher
from modelctl_core.launcher.registry import LauncherRegistry


def test_gemini_launcher_forwards_model_and_arguments():
    launcher = GeminiCliLauncher()

    with (
        patch.object(launcher, "available", return_value=True),
        patch("modelctl_core.launcher.gemini.subprocess.run") as run,
    ):
        launcher.run("auto", ["--sandbox", "--debug"])

    run.assert_called_once_with(
        ["gemini", "--model", "auto", "--sandbox", "--debug"],
        check=True,
    )


def test_gemini_launcher_reports_missing_cli():
    launcher = GeminiCliLauncher()

    with patch.object(launcher, "available", return_value=False):
        try:
            launcher.run("auto")
        except RuntimeError as exc:
            assert "npm install -g @google/gemini-cli" in str(exc)
        else:
            raise AssertionError("Expected RuntimeError")


def test_gemini_launcher_is_registered():
    launcher = LauncherRegistry().get("gemini")

    assert isinstance(launcher, GeminiCliLauncher)
