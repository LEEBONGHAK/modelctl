import pytest

from modelctl_core.auth.types import Credential
from modelctl_core.services.model_service import ModelService


class Repository:
    def __init__(self):
        self.saved = None

    def save_many(self, models):
        self.saved = models


class Provider:
    def __init__(self):
        self.credential = None

    def list_models(self, credential):
        self.credential = credential
        return ["model-a"]


class Providers:
    def __init__(self, provider):
        self.provider = provider

    def get(self, provider_id):
        if provider_id != "openrouter":
            raise KeyError(provider_id)
        return self.provider


class Credentials:
    def __init__(self, token):
        self.token = token

    def load(self, provider_id):
        return self.token


def test_sync_passes_typed_credential_and_saves_models():
    repository = Repository()
    provider = Provider()
    service = ModelService(
        repository=repository,
        provider_registry=Providers(provider),
        credentials=Credentials("secret-token"),
    )

    assert service.sync("openrouter") == 1
    assert provider.credential == Credential(api_key="secret-token")
    assert repository.saved == ["model-a"]


def test_sync_rejects_missing_credential():
    service = ModelService(
        repository=Repository(),
        provider_registry=Providers(Provider()),
        credentials=Credentials(None),
    )

    with pytest.raises(RuntimeError, match="modelctl auth login openrouter"):
        service.sync("openrouter")


def test_sync_rejects_unknown_provider():
    service = ModelService(
        repository=Repository(),
        provider_registry=Providers(Provider()),
        credentials=Credentials("secret-token"),
    )

    with pytest.raises(ValueError, match="Unknown provider"):
        service.sync("unknown")
