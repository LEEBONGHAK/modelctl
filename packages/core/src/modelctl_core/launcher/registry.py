from modelctl_core.launcher.base import Launcher
from modelctl_core.launcher.claude import ClaudeCodeLauncher
from modelctl_core.launcher.codex import CodexCliLauncher
from modelctl_core.launcher.gemini import GeminiCliLauncher


class LauncherRegistry:
    def __init__(self):
        self._launchers: dict[str, Launcher] = {
            "claude": ClaudeCodeLauncher(),
            "gemini": GeminiCliLauncher(),
            "codex": CodexCliLauncher(),
        }

    def get(self, name: str) -> Launcher | None:
        return self._launchers.get(name)

    def list(self) -> list[Launcher]:
        return list(self._launchers.values())
