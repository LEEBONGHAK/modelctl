from unittest.mock import MagicMock, call, patch

import pytest

from modelctl_core.auth.stores.env import EnvironmentStore
from modelctl_core.auth.types import Credential
from modelctl_core.launcher.registry import LauncherRegistry
from modelctl_core.provider.anthropic.client import AnthropicClient
from modelctl_core.provider.anthropic.mapper import AnthropicMapper
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


def anthropic_model(model_id: str = "claude-opus-4-6"):
    return {
        "id": model_id,
        "display_name": "Claude Opus 4.6",
        "max_input_tokens": 200000,
        "capabilities": {
            "image_input": {"supported": True},
            "thinking": {"supported": True},
        },
        "type": "model",
    }


def test_anthropic_client_uses_official_headers_and_paginates():
    client = http_client(
        response(
            {
                "data": [anthropic_model("claude-opus-4-6")],
                "has_more": True,
                "last_id": "claude-opus-4-6",
            }
        ),
        response(
            {
                "data": [anthropic_model("claude-sonnet-4-6")],
                "has_more": False,
                "last_id": "claude-sonnet-4-6",
            }
        ),
    )

    with patch(
        "modelctl_core.provider.anthropic.client.httpx.Client",
        return_value=client,
    ) as client_factory:
        models = AnthropicClient(Credential(api_key=" secret ")).get_models()

    assert [model["id"] for model in models] == [
        "claude-opus-4-6",
        "claude-sonnet-4-6",
    ]
    assert client_factory.call_args.kwargs["headers"] == {
        "x-api-key": "secret",
        "anthropic-version": "2023-06-01",
    }
    assert client_factory.call_args.kwargs["follow_redirects"] is False
    client.get.assert_has_calls(
        [
            call("/models", params={"limit": 1000}),
            call(
                "/models",
                params={"limit": 1000, "after_id": "claude-opus-4-6"},
            ),
        ]
    )


def test_anthropic_client_rejects_invalid_pagination_metadata():
    client = http_client(
        response(
            {
                "data": [anthropic_model()],
                "has_more": True,
                "last_id": None,
            }
        )
    )

    with patch(
        "modelctl_core.provider.anthropic.client.httpx.Client",
        return_value=client,
    ):
        with pytest.raises(ValueError, match="next model cursor"):
            AnthropicClient(Credential(api_key="secret")).get_models()


def test_anthropic_mapper_preserves_catalog_capabilities():
    model = AnthropicMapper().map(anthropic_model())

    assert model.provider == "anthropic"
    assert model.model_id == "claude-opus-4-6"
    assert model.name == "Claude Opus 4.6"
    assert model.context_length == 200000
    assert model.supports_vision is True
    assert model.supports_tools is True
    assert model.supports_reasoning is True
    assert model.prompt_price == 0
    assert model.completion_price == 0


def test_provider_registry_discovers_native_providers():
    registry = ProviderRegistry()
    registry.discover()

    providers = {provider.id: provider.display_name for provider in registry.list()}

    assert providers == {
        "openrouter": "OpenRouter",
        "anthropic": "Anthropic",
        "google": "Google Gemini",
        "openai": "OpenAI",
    }


def test_anthropic_api_key_environment_alias(monkeypatch):
    monkeypatch.delenv("MODELCTL_ANTHROPIC", raising=False)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "official-key")

    assert EnvironmentStore().load("modelctl", "anthropic") == "official-key"


def test_modelctl_environment_name_overrides_anthropic_alias(monkeypatch):
    monkeypatch.setenv("MODELCTL_ANTHROPIC", "modelctl-key")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "official-key")

    assert EnvironmentStore().load("modelctl", "anthropic") == "modelctl-key"


def test_anthropic_catalog_sync_uses_registered_provider():
    class Repository:
        saved = None

        def save_many(self, models):
            self.saved = models

    class Credentials:
        def load(self, provider_id):
            assert provider_id == "anthropic"
            return "secret"

    repository = Repository()
    registry = ProviderRegistry()
    registry.discover()

    with patch(
        "modelctl_core.provider.anthropic.client.AnthropicClient.get_models",
        return_value=[anthropic_model()],
    ):
        count = ModelService(repository, registry, Credentials()).sync("anthropic")

    assert count == 1
    assert repository.saved[0].provider == "anthropic"
    assert repository.saved[0].model_id == "claude-opus-4-6"


def test_anthropic_selection_recommends_and_remediates_to_claude():
    class Config:
        def load(self):
            return {
                "provider": "anthropic",
                "default_model": "claude-opus-4-6",
                "launcher": "codex",
            }

    service = LauncherService(LauncherRegistry(), Config())

    recommendation = service.recommend()
    remediation = service.plan_remediation()

    assert recommendation is not None
    assert recommendation.name == "claude"
    assert "native launcher" in recommendation.reason
    assert remediation.current_name == "codex"
    assert remediation.recommended_name == "claude"
    assert remediation.action_required is True

    with pytest.raises(RuntimeError, match="Strict compatibility check failed"):
        service.check_compatibility(policy="strict")
