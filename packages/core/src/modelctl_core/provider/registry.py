from modelctl_core.provider.anthropic.provider import AnthropicProvider
from modelctl_core.provider.google.provider import GoogleProvider
from modelctl_core.provider.openrouter.provider import OpenRouterProvider


class ProviderRegistry:
    def __init__(self):
        self._providers = {}

    def discover(self):
        self.register(OpenRouterProvider())
        self.register(AnthropicProvider())
        self.register(GoogleProvider())

    def register(self, provider):
        self._providers[provider.id] = provider

    def get(self, provider_id):
        return self._providers[provider_id]

    def list(self):
        return list(self._providers.values())
