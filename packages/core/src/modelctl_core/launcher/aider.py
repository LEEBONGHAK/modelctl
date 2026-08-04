import shutil
import subprocess

from modelctl_core.launcher.base import LaunchRequest, Launcher, LauncherCapabilities


class AiderLauncher(Launcher):
    name = "aider"
    display_name = "Aider"
    capabilities = LauncherCapabilities(
        accepts_any_provider=True,
        translated_providers=frozenset({"openrouter"}),
    )

    def available(self) -> bool:
        return shutil.which("aider") is not None

    def run(self, request: LaunchRequest) -> None:
        if not self.available():
            raise RuntimeError(
                "Aider not found. Install it with: "
                "python -m pip install aider-install && aider-install"
            )

        subprocess.run(
            [
                "aider",
                "--model",
                self._model_name(request.model, request.provider),
                *request.extra_args,
            ],
            check=True,
        )

    @staticmethod
    def _model_name(model: str, provider: str | None) -> str:
        if provider == "openrouter" and not model.startswith("openrouter/"):
            return f"openrouter/{model}"

        return model
