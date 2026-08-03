import shutil
import subprocess

from modelctl_core.launcher.base import Launcher


class ClaudeCodeLauncher(Launcher):
    name = "claude"
    display_name = "Claude Code"

    def available(self) -> bool:
        return shutil.which("claude") is not None

    def run(self, model: str, extra_args: list[str] | None = None) -> None:
        if not self.available():
            raise RuntimeError(
                "Claude Code CLI not found. Install it and run `claude` once to authenticate."
            )

        command = ["claude", "--model", model, *(extra_args or [])]
        subprocess.run(command, check=True)
