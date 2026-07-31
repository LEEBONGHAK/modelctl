import shutil
import subprocess

from modelctl_core.launcher.base import Launcher


class ClaudeCodeLauncher(Launcher):
    name = "claude"
    display_name = "Claude Code"

    def available(self) -> bool:
        return shutil.which("claude") is not None

    def run(self, model: str):
        if not self.available():
            raise RuntimeError("Claude Code CLI not found")

        subprocess.run(
            [
                "claude",
                "--model",
                model,
            ],
            check=True,
        )
