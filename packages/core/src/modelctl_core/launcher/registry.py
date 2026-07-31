from modelctl_core.launcher.claude import (
    ClaudeCodeLauncher,
)


class LauncherRegistry:
    def __init__(self):
        self._launchers = {
            "claude": ClaudeCodeLauncher(),
        }

    def get(self, name: str):
        return self._launchers.get(name)

    def list(self):
        return list(self._launchers.values())
