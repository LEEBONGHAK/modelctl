from modelctl_core.auth.types import Credential
from modelctl_core.provider.base import Provider
from modelctl_core.provider.openai.client import OpenAIModelsClient
from modelctl_core.provider.openai.mapper import OpenAIModelMapper


class OpenAIProvider(Provider):
    id = "openai"
    display_name = "OpenAI"

    def list_models(
        self,
        credential: Credential,
    ):
        client = OpenAIModelsClient(credential)
        mapper = OpenAIModelMapper()
        raw_models = client.get_models()

        return [
            mapper.map(model)
            for model in raw_models
            if mapper.supports_coding(model)
        ]
