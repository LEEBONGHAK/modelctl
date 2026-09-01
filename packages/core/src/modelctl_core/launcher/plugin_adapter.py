from modelctl_sdk import LaunchRequest, LauncherMetadata, LauncherPlugin

from modelctl_core.launcher.base import Launcher


class PluginLauncherAdapter(Launcher):
    """Expose one public SDK launcher plugin through the existing core launcher API."""

    def __init__(self, plugin: LauncherPlugin) -> None:
        self._plugin = plugin
        metadata = plugin.metadata
        self.name = metadata.launcher_id
        self.display_name = metadata.display_name
        self.capabilities = plugin.capabilities
        self.plugin_id = metadata.plugin_id
        self.contract_version = metadata.contract_version

    @property
    def metadata(self) -> LauncherMetadata:
        return self._plugin.metadata

    def available(self) -> bool:
        return self._plugin.available()

    def run(self, request: LaunchRequest) -> None:
        self._plugin.run(request)
