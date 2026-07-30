from modelctl_core.providers.openrouter.client import (
    OpenRouterClient,
)


class OpenRouterProvider(Provider):

    name = "openrouter"
    metadata = ProviderMetadata(
        id="openrouter",
        display_name="OpenRouter",
        homepage="https://openrouter.ai",
    )

    def __init__(self):

        self.client = None

    def login(self, api_key):

        self.client = OpenRouterClient(
            api_key
        )

    def list_models(self):

        return self.client.get_models()