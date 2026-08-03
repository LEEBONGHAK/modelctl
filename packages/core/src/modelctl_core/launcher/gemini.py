import shutil
import subprocess

from modelctl_core.launcher.base import Launcher


class GeminiCliLauncher(Launcher):
    name = "gemini"
    display_name = "Gemini CLI"

    def available(self) -> bool:
        return shutil.which("gemini") is not None

    def run(self, model: str, extra_args: list[str] | None = None) -> None:
        if not self.available():
            raise RuntimeError(
                "Gemini CLI not found. Install it with: "
                "npm install -g @google/gemini-cli"
            )

        subprocess.run(
            ["gemini", "--model", model, *(extra_args or [])],
            check=True,
        )
