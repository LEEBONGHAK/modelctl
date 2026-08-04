from unittest.mock import patch

from modelctl_core.launcher.base import LaunchRequest
from modelctl_core.launcher.codex import CodexCliLauncher
from modelctl_core.launcher.registry import LauncherRegistry


def test_codex_launcher_forwards_model_and_arguments():
    launcher = CodexCliLauncher()
    request = LaunchRequest.create(
        "gpt-5.6",
        extra_args=["--sandbox", "workspace-write"],
    )

    with (
        patch.object(launcher, "available", return_value=True),
        patch("modelctl_core.launcher.codex.subprocess.run") as run,
    ):
        launcher.run(request)

    run.assert_called_once_with(
        ["codex", "--model", "gpt-5.6", "--sandbox", "workspace-write"],
        check=True,
    )


def test_codex_launcher_reports_missing_cli():
    launcher = CodexCliLauncher()

    with patch.object(launcher, "available", return_value=False):
        try:
            launcher.run(LaunchRequest.create("gpt-5.6"))
        except RuntimeError as exc:
            assert "npm install -g @openai/codex" in str(exc)
        else:
            raise AssertionError("Expected RuntimeError")


def test_codex_launcher_is_registered():
    launcher = LauncherRegistry().get("codex")

    assert isinstance(launcher, CodexCliLauncher)
