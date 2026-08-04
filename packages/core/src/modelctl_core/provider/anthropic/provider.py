from modelctl_core.auth.types import Credential
from modelctl_core.provider.anthropic.client import AnthropicClient
from modelctl_core.provider.anthropic.mapper import AnthropicMapper
from modelctl_core.provider.base import Provider


class AnthropicProvider(Provider):
    id = "anthropic"
    display_name = "Anthropic"

    def list_models(self, credential: Credential):
        client = AnthropicClient(credential)
        mapper = AnthropicMapper()
        return [mapper.map(model) for model in client.get_models()]
