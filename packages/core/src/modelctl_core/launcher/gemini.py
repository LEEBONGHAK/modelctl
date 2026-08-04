import shutil
import subprocess

from modelctl_core.launcher.base import LaunchRequest, Launcher, LauncherCapabilities


class GeminiCliLauncher(Launcher):
    name = "gemini"
    display_name = "Gemini CLI"
    capabilities = LauncherCapabilities(native_provider="google")

    def available(self) -> bool:
        return shutil.which("gemini") is not None

    def run(self, request: LaunchRequest) -> None:
        if not self.available():
            raise RuntimeError(
                "Gemini CLI not found. Install it with: "
                "npm install -g @google/gemini-cli"
            )

        subprocess.run(
            ["gemini", "--model", request.model, *request.extra_args],
            check=True,
        )
