from modelctl_core.launcher.aider import AiderLauncher
from modelctl_core.launcher.base import Launcher
from modelctl_core.launcher.claude import ClaudeCodeLauncher
from modelctl_core.launcher.codex import CodexCliLauncher
from modelctl_core.launcher.discovery import (
    LauncherDiscoveryRecord,
    discover_launcher_plugins,
)
from modelctl_core.launcher.gemini import GeminiCliLauncher


class LauncherRegistry:
    def __init__(self, entry_points=None):
        self._launchers: dict[str, Launcher] = {
            "claude": ClaudeCodeLauncher(),
            "gemini": GeminiCliLauncher(),
            "codex": CodexCliLauncher(),
            "aider": AiderLauncher(),
        }
        self._diagnostics = [
            LauncherDiscoveryRecord(
                launcher_id=launcher.name,
                display_name=launcher.display_name,
                plugin_id=launcher.plugin_id,
                source="builtin:modelctl",
                status="loaded",
            )
            for launcher in self._launchers.values()
        ]

        plugins, records = discover_launcher_plugins(
            reserved_ids=set(self._launchers),
            entry_points=entry_points,
        )
        for launcher in plugins:
            self._launchers[launcher.name] = launcher
        self._diagnostics.extend(records)

    def get(self, name: str) -> Launcher | None:
        return self._launchers.get(name)

    def list(self) -> list[Launcher]:
        return list(self._launchers.values())

    def diagnostics(self) -> list[LauncherDiscoveryRecord]:
        return list(self._diagnostics)
