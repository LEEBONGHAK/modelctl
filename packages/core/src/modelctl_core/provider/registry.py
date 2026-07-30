from modelctl_core.providers.openrouter.provider import OpenRouterProvider


class ProviderRegistry:

    def __init__(self):
        self._providers = {}

    def discover(self):
        self.register(OpenRouterProvider())
    
    def register(self, provider):
        self._providers[provider.name] = provider

    def get(self, name):
        return self._providers[name]

    def list(self):
        return list(self._providers.values())