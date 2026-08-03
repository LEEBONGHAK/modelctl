import shutil
import subprocess

from modelctl_core.launcher.base import Launcher


class AiderLauncher(Launcher):
    name = "aider"
    display_name = "Aider"

    def available(self) -> bool:
        return shutil.which("aider") is not None

    def run(
        self,
        model: str,
        extra_args: list[str] | None = None,
        provider: str | None = None,
    ) -> None:
        if not self.available():
            raise RuntimeError(
                "Aider not found. Install it with: "
                "python -m pip install aider-install && aider-install"
            )

        subprocess.run(
            [
                "aider",
                "--model",
                self._model_name(model, provider),
                *(extra_args or []),
            ],
            check=True,
        )

    @staticmethod
    def _model_name(model: str, provider: str | None) -> str:
        if provider == "openrouter" and not model.startswith("openrouter/"):
            return f"openrouter/{model}"

        return model
