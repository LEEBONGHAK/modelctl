from importlib.metadata import entry_points


class PluginLoader:
    PROVIDER_GROUP = "modelctl.providers"

    LAUNCHER_GROUP = "modelctl.launchers"

    def load_providers(self):
        plugins = entry_points(group=self.PROVIDER_GROUP)

        return [plugin.load() for plugin in plugins]

    def load_launchers(self):
        plugins = entry_points(group=self.LAUNCHER_GROUP)

        return [plugin.load() for plugin in plugins]
