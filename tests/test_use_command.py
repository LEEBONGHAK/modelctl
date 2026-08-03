from click import unstyle
from typer.testing import CliRunner

from modelctl_cli.context import container
from modelctl_cli.main import app


runner = CliRunner()


class StubConfig:
    def __init__(self):
        self.updated = None

    def update_model(self, provider, model):
        self.updated = (provider, model)


class StubSelection:
    def __init__(self, validation_error=None):
        self.validation_error = validation_error
        self.validated = None
        self.interactive_calls = []

    def validate(self, provider, model):
        self.validated = (provider, model)
        if self.validation_error:
            raise ValueError(self.validation_error)
        return provider, model

    def select_provider(self):
        self.interactive_calls.append("provider")
        return "openrouter"

    def select_model(self, provider):
        self.interactive_calls.append(("model", provider))
        return "anthropic/claude-sonnet-4"


def install_stubs(monkeypatch, selection):
    config = StubConfig()
    monkeypatch.setattr(container, "selection_service", lambda: selection)
    monkeypatch.setattr(container, "config", config)
    return config


def normalized(text):
    return " ".join(unstyle(text).split())


def test_use_accepts_provider_and_model_without_prompting(monkeypatch):
    selection = StubSelection()
    config = install_stubs(monkeypatch, selection)

    result = runner.invoke(
        app,
        [
            "use",
            "--provider",
            "openrouter",
            "--model",
            "anthropic/claude-sonnet-4",
        ],
    )

    assert result.exit_code == 0
    assert selection.validated == (
        "openrouter",
        "anthropic/claude-sonnet-4",
    )
    assert selection.interactive_calls == []
    assert config.updated == (
        "openrouter",
        "anthropic/claude-sonnet-4",
    )
    assert "Default model updated" in result.stdout


def test_use_requires_provider_and_model_together():
    result = runner.invoke(app, ["use", "--provider", "openrouter"])

    assert result.exit_code == 2
    assert "Use --provider and --model together" in normalized(result.stderr)


def test_use_reports_unknown_direct_selection(monkeypatch):
    selection = StubSelection("Unknown model for openrouter: missing/model")
    config = install_stubs(monkeypatch, selection)

    result = runner.invoke(
        app,
        [
            "use",
            "-p",
            "openrouter",
            "-m",
            "missing/model",
        ],
    )

    assert result.exit_code == 2
    assert "Unknown model for openrouter" in normalized(result.stderr)
    assert config.updated is None


def test_use_preserves_interactive_selection(monkeypatch):
    selection = StubSelection()
    config = install_stubs(monkeypatch, selection)

    result = runner.invoke(app, ["use"])

    assert result.exit_code == 0
    assert selection.validated is None
    assert selection.interactive_calls == [
        "provider",
        ("model", "openrouter"),
    ]
    assert config.updated == (
        "openrouter",
        "anthropic/claude-sonnet-4",
    )
