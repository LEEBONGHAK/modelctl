import shutil
import subprocess

from modelctl_core.launcher.base import LaunchRequest, Launcher, LauncherCapabilities


class CodexCliLauncher(Launcher):
    name = "codex"
    display_name = "Codex CLI"
    capabilities = LauncherCapabilities(native_provider="openai")

    def available(self) -> bool:
        return shutil.which("codex") is not None

    def run(self, request: LaunchRequest) -> None:
        if not self.available():
            raise RuntimeError(
                "Codex CLI not found. Install it with: npm install -g @openai/codex"
            )

        subprocess.run(
            ["codex", "--model", request.model, *request.extra_args],
            check=True,
        )
