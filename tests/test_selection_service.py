from types import SimpleNamespace

from modelctl_core.services.selection_service import SelectionService


class StubRegistry:
    def list(self):
        return [SimpleNamespace(id="openrouter", display_name="OpenRouter")]


class StubRepository:
    def list_by_provider(self, provider_id):
        assert provider_id == "openrouter"
        return [SimpleNamespace(model_id="anthropic/claude-sonnet-4", favorite=True)]


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
