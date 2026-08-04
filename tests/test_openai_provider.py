from unittest.mock import MagicMock, call, patch

import pytest

from modelctl_core.auth.stores.env import EnvironmentStore
from modelctl_core.auth.types import Credential
from modelctl_core.launcher.registry import LauncherRegistry
from modelctl_core.provider.openai.client import OpenAIModelsClient
from modelctl_core.provider.openai.mapper import OpenAIModelMapper
from modelctl_core.provider.registry import ProviderRegistry
from modelctl_core.services.launcher_service import LauncherService
from modelctl_core.services.model_service import ModelService


def response(payload):
    result = MagicMock()
    result.json.return_value = payload
    return result


def http_client(*responses):
    client = MagicMock()
    client.__enter__.return_value = client
    client.get.side_effect = responses
    return client


def openai_model(model_id: str = "gpt-5.6"):
    return {
        "id": model_id,
        "object": "model",
        "created": 1770000000,
        "owned_by": "openai",
    }


def test_openai_client_uses_bearer_auth_and_fixed_endpoint():
    client = http_client(response({"object": "list", "data": [openai_model()]}))

    with patch(
        "modelctl_core.provider.openai.client.httpx.Client",
        return_value=client,
    ) as client_factory:
        models = OpenAIModelsClient(Credential(api_key=" secret ")).get_models()

    assert [model["id"] for model in models] == ["gpt-5.6"]
    assert client_factory.call_args.kwargs["base_url"] == "https://api.openai.com/v1"
    assert client_factory.call_args.kwargs["headers"] == {
        "Authorization": "Bearer secret"
    }
    assert client_factory.call_args.kwargs["follow_redirects"] is False
    client.get.assert_has_calls([call("/models")])


def test_openai_client_rejects_invalid_model_response():
    client = http_client(response({"object": "list", "data": None}))

    with patch(
        "modelctl_core.provider.openai.client.httpx.Client",
        return_value=client,
    ):
        with pytest.raises(ValueError, match="invalid model response"):
            OpenAIModelsClient(Credential(api_key="secret")).get_models()


def test_openai_mapper_preserves_only_known_catalog_fields():
    model = OpenAIModelMapper().map(openai_model("gpt-5.6"))

    assert model.provider == "openai"
    assert model.model_id == "gpt-5.6"
    assert model.name == "gpt-5.6"
    assert model.context_length == 0
    assert model.supports_vision is False
    assert model.supports_tools is True
    assert model.supports_reasoning is True
    assert model.prompt_price == 0
    assert model.completion_price == 0


def test_openai_provider_excludes_non_coding_model_families():
    registry = ProviderRegistry()
    registry.discover()
    provider = registry.get("openai")

    with patch(
        "modelctl_core.provider.openai.client.OpenAIModelsClient.get_models",
        return_value=[
            openai_model("gpt-5.6"),
            openai_model("gpt-5.3-codex"),
            openai_model("codex-mini-latest"),
            openai_model("text-embedding-3-large"),
            openai_model("gpt-image-2"),
            openai_model("gpt-realtime-1.5"),
            openai_model("omni-moderation-latest"),
            openai_model("ft:gpt-4.1:example"),
        ],
    ):
        models = provider.list_models(Credential(api_key="secret"))

    assert [model.model_id for model in models] == [
        "gpt-5.6",
        "gpt-5.3-codex",
        "codex-mini-latest",
    ]


def test_openai_api_key_environment_alias(monkeypatch):
    monkeypatch.delenv("MODELCTL_OPENAI", raising=False)
    monkeypatch.setenv("OPENAI_API_KEY", "official-key")

    assert EnvironmentStore().load("modelctl", "openai") == "official-key"


def test_modelctl_environment_name_overrides_openai_alias(monkeypatch):
    monkeypatch.setenv("MODELCTL_OPENAI", "modelctl-key")
    monkeypatch.setenv("OPENAI_API_KEY", "official-key")

    assert EnvironmentStore().load("modelctl", "openai") == "modelctl-key"


def test_openai_catalog_sync_uses_registered_provider():
    class Repository:
        saved = None

        def save_many(self, models):
            self.saved = models

    class Credentials:
        def load(self, provider_id):
            assert provider_id == "openai"
            return "secret"

    repository = Repository()
    registry = ProviderRegistry()
    registry.discover()

    with patch(
        "modelctl_core.provider.openai.client.OpenAIModelsClient.get_models",
        return_value=[openai_model()],
    ):
        count = ModelService(repository, registry, Credentials()).sync("openai")

    assert count == 1
    assert repository.saved[0].provider == "openai"
    assert repository.saved[0].model_id == "gpt-5.6"


def test_openai_selection_recommends_and_remediates_to_codex():
    class Config:
        def load(self):
            return {
                "provider": "openai",
                "default_model": "gpt-5.6",
                "launcher": "gemini",
            }

    service = LauncherService(LauncherRegistry(), Config())

    recommendation = service.recommend()
    remediation = service.plan_remediation()

    assert recommendation is not None
    assert recommendation.name == "codex"
    assert "native launcher" in recommendation.reason
    assert remediation.current_name == "gemini"
    assert remediation.recommended_name == "codex"
    assert remediation.action_required is True

    with pytest.raises(RuntimeError, match="Strict compatibility check failed"):
        service.check_compatibility(policy="strict")
