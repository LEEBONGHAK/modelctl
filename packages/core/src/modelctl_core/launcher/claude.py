import shutil
import subprocess

from modelctl_core.launcher.base import LaunchRequest, Launcher, LauncherCapabilities


class ClaudeCodeLauncher(Launcher):
    name = "claude"
    display_name = "Claude Code"
    capabilities = LauncherCapabilities(native_provider="anthropic")

    def available(self) -> bool:
        return shutil.which("claude") is not None

    def run(self, request: LaunchRequest) -> None:
        if not self.available():
            raise RuntimeError(
                "Claude Code CLI not found. Install it and run `claude` once to authenticate."
            )

        command = ["claude", "--model", request.model, *request.extra_args]
        subprocess.run(command, check=True)
