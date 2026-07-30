from modelctl_core.providers.openrouter.provider import OpenRouterProvider


class ProviderRegistry:

    def __init__(self):
        registry.register(
            OpenRouterProvider
        )

    def get(self, name):

        return registry.get(name)

    def all(self):

        return self.providers.values()