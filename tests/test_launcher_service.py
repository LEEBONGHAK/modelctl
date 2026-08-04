from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from modelctl_core.launcher.base import LaunchRequest, LauncherCapabilities
from modelctl_core.services.launcher_service import LauncherService


def configured(
    provider="openrouter",
    launcher="claude",
    compatibility_policy: str | None = None,
):
    config = Mock()
    values = {
        "launcher": launcher,
        "provider": provider,
        "default_model": "anthropic/claude-sonnet-4",
    }
    if compatibility_policy is not None:
        values["compatibility_policy"] = compatibility_policy
    config.load.return_value = values
    return config


def recommendation_launcher(
    name: str,
    display_name: str,
    native_provider: str | None,
    installed: bool = True,
    translated_providers: frozenset[str] = frozenset(),
):
    return SimpleNamespace(
        name=name,
        display_name=display_name,
        capabilities=LauncherCapabilities(
            native_provider=native_provider,
            accepts_any_provider=name == "aider",
            translated_providers=translated_providers,
        ),
        available=lambda: installed,
    )


def mismatched_service(config=None):
    launcher = Mock()
    launcher.compatibility_warning.return_value = "Potential mismatch"
    registry = Mock()
    registry.get.return_value = launcher
    return LauncherService(registry, config or configured()), launcher


def test_launcher_service_builds_immutable_execution_request():
    launcher = Mock()
    registry = Mock()
    registry.get.return_value = launcher
    config = configured(launcher="aider")
    extra_args = ["--no-auto-commits"]

    LauncherService(registry, config).run(extra_args)
    extra_args.append("--dirty")

    registry.get.assert_called_once_with("aider")
    launcher.run.assert_called_once_with(
        LaunchRequest(
            model="anthropic/claude-sonnet-4",
            provider="openrouter",
            extra_args=("--no-auto-commits",),
        )
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
        LaunchRequest(model="claude-sonnet-4")
    )


def test_launcher_service_returns_compatibility_warning():
    service, launcher = mismatched_service()

    warning = service.compatibility_warning()

    assert warning == "Potential mismatch"
    launcher.compatibility_warning.assert_called_once_with(
        LaunchRequest(
            model="anthropic/claude-sonnet-4",
            provider="openrouter",
        )
    )


def test_compatibility_check_defaults_to_warn_policy():
    service, _ = mismatched_service()

    warning = service.check_compatibility()

    assert warning == "Potential mismatch"
    assert service.compatibility_policy() == "warn"


def test_compatibility_check_uses_persisted_strict_policy():
    service, _ = mismatched_service(configured(compatibility_policy="strict"))

    with pytest.raises(RuntimeError, match="Strict compatibility check failed"):
        service.check_compatibility()


def test_explicit_warn_policy_overrides_persisted_strict_policy():
    service, _ = mismatched_service(configured(compatibility_policy="strict"))

    warning = service.check_compatibility(policy="warn")

    assert warning == "Potential mismatch"


def test_explicit_strict_policy_overrides_persisted_warn_policy():
    service, _ = mismatched_service(configured(compatibility_policy="warn"))

    with pytest.raises(RuntimeError, match="Strict compatibility check failed"):
        service.check_compatibility(policy="strict")


def test_compatibility_check_rejects_invalid_persisted_policy():
    service, _ = mismatched_service(configured(compatibility_policy="automatic"))

    with pytest.raises(RuntimeError, match="Invalid compatibility policy"):
        service.check_compatibility()


def test_recommendation_uses_translating_launcher_for_openrouter():
    registry = Mock()
    registry.list.return_value = [
        recommendation_launcher("claude", "Claude Code", "anthropic"),
        recommendation_launcher(
            "aider",
            "Aider",
            None,
            translated_providers=frozenset({"openrouter"}),
        ),
    ]

    recommendation = LauncherService(registry, configured()).recommend()

    assert recommendation is not None
    assert recommendation.name == "aider"
    assert recommendation.provider == "openrouter"
    assert recommendation.installed is True
    assert recommendation.active is False
    assert recommendation.changed is False
    assert "translates openrouter" in recommendation.reason


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
        recommendation_launcher(
            "aider",
            "Aider",
            None,
            installed=True,
            translated_providers=frozenset({"openrouter"}),
        ),
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
        recommendation_launcher(
            "aider",
            "Aider",
            None,
            installed=True,
            translated_providers=frozenset({"openrouter"}),
        ),
    ]
    config = configured(launcher="aider")

    recommendation = LauncherService(registry, config).apply_recommendation()

    assert recommendation.active is True
    assert recommendation.changed is False
    config.update.assert_not_called()


def test_apply_recommendation_refuses_unavailable_launcher():
    registry = Mock()
    registry.list.return_value = [
        recommendation_launcher(
            "aider",
            "Aider",
            None,
            installed=False,
            translated_providers=frozenset({"openrouter"}),
        ),
    ]
    config = configured()

    with pytest.raises(RuntimeError, match="not installed"):
        LauncherService(registry, config).apply_recommendation()

    config.update.assert_not_called()
