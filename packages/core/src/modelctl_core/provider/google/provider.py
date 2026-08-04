from modelctl_core.auth.types import Credential
from modelctl_core.provider.base import Provider
from modelctl_core.provider.google.client import GoogleModelsClient
from modelctl_core.provider.google.mapper import GoogleModelMapper


class GoogleProvider(Provider):
    id = "google"
    display_name = "Google Gemini"

    def list_models(
        self,
        credential: Credential,
    ):
        client = GoogleModelsClient(credential)
        mapper = GoogleModelMapper()
        raw_models = client.get_models()

        return [
            mapper.map(model)
            for model in raw_models
            if mapper.supports_generation(model)
        ]
