from types import SimpleNamespace

import pytest

from modelctl_core.services.selection_service import SelectionService


class StubRegistry:
    def list(self):
        return [SimpleNamespace(id="openrouter", display_name="OpenRouter")]


class StubRepository:
    def __init__(self, model=None):
        self.model = model

    def list_by_provider(self, provider_id):
        assert provider_id == "openrouter"
        return [SimpleNamespace(model_id="anthropic/claude-sonnet-4", favorite=True)]

    def get_by_provider(self, provider_id, model_id):
        if (
            provider_id == "openrouter"
            and model_id == "anthropic/claude-sonnet-4"
        ):
            return self.model
        return None


class StubSelector:
    def select(self, title, choices):
        if title == "Select Provider":
            assert choices == ["OpenRouter"]
            return "OpenRouter"

        assert choices == ["★ anthropic/claude-sonnet-4"]
        return choices[0]


def test_selection_returns_provider_id_and_clean_model_id():
    service = SelectionService(StubRegistry(), StubRepository(), StubSelector())

    provider_id = service.select_provider()
    model_id = service.select_model(provider_id)

    assert provider_id == "openrouter"
    assert model_id == "anthropic/claude-sonnet-4"


def test_validate_accepts_synced_provider_model_pair():
    model = SimpleNamespace(model_id="anthropic/claude-sonnet-4")
    service = SelectionService(
        StubRegistry(),
        StubRepository(model),
        selector=None,
    )

    result = service.validate("openrouter", "anthropic/claude-sonnet-4")

    assert result == ("openrouter", "anthropic/claude-sonnet-4")


def test_validate_rejects_unknown_provider_and_model():
    service = SelectionService(StubRegistry(), StubRepository(), selector=None)

    with pytest.raises(ValueError, match="Unknown provider: missing"):
        service.validate("missing", "some/model")

    with pytest.raises(ValueError, match="modelctl models sync openrouter"):
        service.validate("openrouter", "missing/model")
