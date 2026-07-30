from modelctl_core.plugins.loader import (
    PluginLoader,
)


class PluginRegistry:
    def __init__(self):
        self.loader = PluginLoader()
        self.providers = []
        self.launchers = []

    def discover(self):
        self.providers = self.loader.load_providers()
        self.launchers = self.loader.load_launchers()

    def list_providers(self):
        return self.providers

    def list_launchers(self):
        return self.launchers
