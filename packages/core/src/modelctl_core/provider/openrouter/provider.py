from modelctl_core.auth.types import Credential
from modelctl_core.provider.base import Provider

from modelctl_core.provider.openrouter.client import OpenRouterClient
from modelctl_core.provider.openrouter.mapper import OpenRouterMapper


class OpenRouterProvider(Provider):
    id = "openrouter"
    display_name = "OpenRouter"

    def list_models(
        self,
        credential: Credential,
    ):

        client = OpenRouterClient(credential)

        mapper = OpenRouterMapper()

        raw = client.get_models()

        return [mapper.map(model) for model in raw]
