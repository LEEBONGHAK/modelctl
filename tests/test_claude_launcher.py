from unittest.mock import patch

from modelctl_core.launcher.claude import ClaudeCodeLauncher


def test_claude_launcher_forwards_model_and_arguments():
    launcher = ClaudeCodeLauncher()

    with (
        patch.object(launcher, "available", return_value=True),
        patch("modelctl_core.launcher.claude.subprocess.run") as run,
    ):
        launcher.run("sonnet", ["--continue", "--verbose"])

    run.assert_called_once_with(
        ["claude", "--model", "sonnet", "--continue", "--verbose"],
        check=True,
    )


def test_claude_launcher_reports_missing_cli():
    launcher = ClaudeCodeLauncher()

    with patch.object(launcher, "available", return_value=False):
        try:
            launcher.run("sonnet")
        except RuntimeError as exc:
            assert "Claude Code CLI not found" in str(exc)
        else:
            raise AssertionError("Expected RuntimeError")
