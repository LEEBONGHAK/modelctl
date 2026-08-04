from unittest.mock import MagicMock, call, patch

import pytest

from modelctl_core.auth.stores.env import EnvironmentStore
from modelctl_core.auth.types import Credential
from modelctl_core.launcher.registry import LauncherRegistry
from modelctl_core.provider.google.client import GoogleModelsClient
from modelctl_core.provider.google.mapper import GoogleModelMapper
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


def google_model(
    model_id: str = "gemini-3.5-flash",
    methods: list[str] | None = None,
):
    return {
        "name": f"models/{model_id}",
        "baseModelId": model_id,
        "version": "3.5",
        "displayName": "Gemini 3.5 Flash",
        "inputTokenLimit": 1048576,
        "outputTokenLimit": 65536,
        "supportedGenerationMethods": methods or ["generateContent"],
        "thinking": True,
    }


def test_google_client_uses_official_header_and_paginates():
    client = http_client(
        response(
            {
                "models": [google_model("gemini-3.5-flash")],
                "nextPageToken": "next-page",
            }
        ),
        response({"models": [google_model("gemini-3.1-pro")]}),
    )

    with patch(
        "modelctl_core.provider.google.client.httpx.Client",
        return_value=client,
    ) as client_factory:
        models = GoogleModelsClient(Credential(api_key=" secret ")).get_models()

    assert [model["baseModelId"] for model in models] == [
        "gemini-3.5-flash",
        "gemini-3.1-pro",
    ]
    assert client_factory.call_args.kwargs["headers"] == {
        "x-goog-api-key": "secret"
    }
    assert client_factory.call_args.kwargs["follow_redirects"] is False
    client.get.assert_has_calls(
        [
            call("/models", params={"pageSize": 1000}),
            call(
                "/models",
                params={"pageSize": 1000, "pageToken": "next-page"},
            ),
        ]
    )


def test_google_client_rejects_repeated_page_token():
    client = http_client(
        response({"models": [google_model()], "nextPageToken": "same"}),
        response({"models": [google_model()], "nextPageToken": "same"}),
    )

    with patch(
        "modelctl_core.provider.google.client.httpx.Client",
        return_value=client,
    ):
        with pytest.raises(ValueError, match="repeated a model pagination token"):
            GoogleModelsClient(Credential(api_key="secret")).get_models()


def test_google_mapper_normalizes_resource_name_and_capabilities():
    model = GoogleModelMapper().map(google_model())

    assert model.provider == "google"
    assert model.model_id == "gemini-3.5-flash"
    assert model.name == "Gemini 3.5 Flash"
    assert model.context_length == 1048576
    assert model.supports_vision is False
    assert model.supports_tools is True
    assert model.supports_reasoning is True
    assert model.prompt_price == 0
    assert model.completion_price == 0


def test_google_provider_excludes_non_generation_models():
    registry = ProviderRegistry()
    registry.discover()
    provider = registry.get("google")

    with patch(
        "modelctl_core.provider.google.client.GoogleModelsClient.get_models",
        return_value=[
            google_model(),
            google_model("text-embedding-004", ["embedContent"]),
        ],
    ):
        models = provider.list_models(Credential(api_key="secret"))

    assert [model.model_id for model in models] == ["gemini-3.5-flash"]


def test_google_environment_alias_precedence(monkeypatch):
    monkeypatch.delenv("MODELCTL_GOOGLE", raising=False)
    monkeypatch.setenv("GEMINI_API_KEY", "gemini-key")
    monkeypatch.setenv("GOOGLE_API_KEY", "google-key")

    assert EnvironmentStore().load("modelctl", "google") == "google-key"


def test_modelctl_environment_name_overrides_google_aliases(monkeypatch):
    monkeypatch.setenv("MODELCTL_GOOGLE", "modelctl-key")
    monkeypatch.setenv("GOOGLE_API_KEY", "google-key")
    monkeypatch.setenv("GEMINI_API_KEY", "gemini-key")

    assert EnvironmentStore().load("modelctl", "google") == "modelctl-key"


def test_google_catalog_sync_uses_registered_provider():
    class Repository:
        saved = None

        def save_many(self, models):
            self.saved = models

    class Credentials:
        def load(self, provider_id):
            assert provider_id == "google"
            return "secret"

    repository = Repository()
    registry = ProviderRegistry()
    registry.discover()

    with patch(
        "modelctl_core.provider.google.client.GoogleModelsClient.get_models",
        return_value=[google_model()],
    ):
        count = ModelService(repository, registry, Credentials()).sync("google")

    assert count == 1
    assert repository.saved[0].provider == "google"
    assert repository.saved[0].model_id == "gemini-3.5-flash"


def test_google_selection_recommends_and_remediates_to_gemini():
    class Config:
        def load(self):
            return {
                "provider": "google",
                "default_model": "gemini-3.5-flash",
                "launcher": "claude",
            }

    service = LauncherService(LauncherRegistry(), Config())

    recommendation = service.recommend()
    remediation = service.plan_remediation()

    assert recommendation is not None
    assert recommendation.name == "gemini"
    assert "native launcher" in recommendation.reason
    assert remediation.current_name == "claude"
    assert remediation.recommended_name == "gemini"
    assert remediation.action_required is True

    with pytest.raises(RuntimeError, match="Strict compatibility check failed"):
        service.check_compatibility(policy="strict")
