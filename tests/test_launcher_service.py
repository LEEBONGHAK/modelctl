from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from modelctl_core.services.launcher_service import LauncherService


def configured(provider="openrouter", launcher="claude"):
    config = Mock()
    config.load.return_value = {
        "launcher": launcher,
        "provider": provider,
        "default_model": "anthropic/claude-sonnet-4",
    }
    return config


def recommendation_launcher(
    name: str,
    display_name: str,
    native_provider: str | None,
    installed: bool = True,
):
    return SimpleNamespace(
        name=name,
        display_name=display_name,
        native_provider=native_provider,
        available=lambda: installed,
    )


def test_launcher_service_forwards_provider_context():
    launcher = Mock()
    registry = Mock()
    registry.get.return_value = launcher
    config = configured(launcher="aider")

    LauncherService(registry, config).run(["--no-auto-commits"])

    registry.get.assert_called_once_with("aider")
    launcher.run.assert_called_once_with(
        "anthropic/claude-sonnet-4",
        ["--no-auto-commits"],
        provider="openrouter",
    )


def test_launcher_service_preserves_execution_without_provider_context():
    launcher = Mock()
    registry = Mock()
    registry.get.return_value = launcher
    config = Mock()
    config.load.return_value = {
        "launcher": "claude",
        "default_model": "claude-sonnet-4",
    }

    LauncherService(registry, config).run()

    launcher.run.assert_called_once_with(
        "claude-sonnet-4",
        None,
        provider=None,
    )


def test_launcher_service_returns_compatibility_warning():
    launcher = Mock()
    launcher.compatibility_warning.return_value = "Potential mismatch"
    registry = Mock()
    registry.get.return_value = launcher
    config = configured()

    warning = LauncherService(registry, config).compatibility_warning()

    assert warning == "Potential mismatch"
    launcher.compatibility_warning.assert_called_once_with(
        "openrouter",
        "anthropic/claude-sonnet-4",
    )


def test_recommendation_uses_aider_for_openrouter():
    registry = Mock()
    registry.list.return_value = [
        recommendation_launcher("claude", "Claude Code", "anthropic"),
        recommendation_launcher("aider", "Aider", None),
    ]

    recommendation = LauncherService(registry, configured()).recommend()

    assert recommendation is not None
    assert recommendation.name == "aider"
    assert recommendation.provider == "openrouter"
    assert recommendation.installed is True
    assert recommendation.active is False
    assert recommendation.changed is False
    assert "translates OpenRouter" in recommendation.reason


def test_recommendation_uses_native_launcher_for_provider():
    registry = Mock()
    registry.list.return_value = [
        recommendation_launcher("claude", "Claude Code", "anthropic"),
        recommendation_launcher("aider", "Aider", None),
    ]

    recommendation = LauncherService(
        registry,
        configured(provider="anthropic", launcher="aider"),
    ).recommend()

    assert recommendation is not None
    assert recommendation.name == "claude"
    assert recommendation.active is False
    assert "native launcher" in recommendation.reason


def test_recommendation_returns_none_for_unknown_provider():
    registry = Mock()
    registry.list.return_value = [
        recommendation_launcher("claude", "Claude Code", "anthropic"),
        recommendation_launcher("aider", "Aider", None),
    ]

    recommendation = LauncherService(
        registry,
        configured(provider="unknown"),
    ).recommend()

    assert recommendation is None


def test_apply_recommendation_persists_and_reports_active_launcher():
    registry = Mock()
    registry.list.return_value = [
        recommendation_launcher("aider", "Aider", None, installed=True),
    ]
    config = configured()

    recommendation = LauncherService(registry, config).apply_recommendation()

    assert recommendation.name == "aider"
    assert recommendation.active is True
    assert recommendation.changed is True
    config.update.assert_called_once_with(launcher="aider")


def test_apply_recommendation_keeps_already_active_launcher_unchanged():
    registry = Mock()
    registry.list.return_value = [
        recommendation_launcher("aider", "Aider", None, installed=True),
    ]
    config = configured(launcher="aider")

    recommendation = LauncherService(registry, config).apply_recommendation()

    assert recommendation.active is True
    assert recommendation.changed is False
    config.update.assert_not_called()


def test_apply_recommendation_refuses_unavailable_launcher():
    registry = Mock()
    registry.list.return_value = [
        recommendation_launcher("aider", "Aider", None, installed=False),
    ]
    config = configured()

    with pytest.raises(RuntimeError, match="not installed"):
        LauncherService(registry, config).apply_recommendation()

    config.update.assert_not_called()
