import shutil
import subprocess

from modelctl_core.launcher.base import Launcher


class CodexCliLauncher(Launcher):
    name = "codex"
    display_name = "Codex CLI"
    native_provider = "openai"

    def available(self) -> bool:
        return shutil.which("codex") is not None

    def run(
        self,
        model: str,
        extra_args: list[str] | None = None,
        provider: str | None = None,
    ) -> None:
        del provider

        if not self.available():
            raise RuntimeError(
                "Codex CLI not found. Install it with: npm install -g @openai/codex"
            )

        subprocess.run(
            ["codex", "--model", model, *(extra_args or [])],
            check=True,
        )
