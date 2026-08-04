from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from modelctl_core.launcher.base import LauncherCapabilities
from modelctl_core.services.launcher_service import LauncherService


def configured(launcher: str = "claude"):
    config = Mock()
    config.load.return_value = {
        "provider": "openrouter",
        "default_model": "anthropic/claude-sonnet-4",
        "launcher": launcher,
    }
    return config


def fake_launcher(
    name: str,
    display_name: str,
    *,
    native_provider: str | None = None,
    translated_providers: frozenset[str] = frozenset(),
    installed: bool = True,
    warning: str | None = None,
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
        compatibility_warning=Mock(return_value=warning),
    )


def remediation_service(*, recommended_installed: bool = True):
    current = fake_launcher(
        "claude",
        "Claude Code",
        native_provider="anthropic",
        warning="Potential mismatch",
    )
    recommended = fake_launcher(
        "aider",
        "Aider",
        translated_providers=frozenset({"openrouter"}),
        installed=recommended_installed,
    )
    registry = Mock()
    registry.get.return_value = current
    registry.list.return_value = [current, recommended]
    config = configured()
    return LauncherService(registry, config), config


def test_remediation_plan_is_read_only_and_recommends_translating_launcher():
    service, config = remediation_service()

    remediation = service.plan_remediation()

    assert remediation.current_name == "claude"
    assert remediation.recommended_name == "aider"
    assert remediation.recommended_installed is True
    assert remediation.action_required is True
    assert remediation.changed is False
    assert remediation.warning == "Potential mismatch"
    assert "translates openrouter" in remediation.reason
    config.update.assert_not_called()


def test_remediation_plan_reports_no_change_for_compatible_launcher():
    current = fake_launcher(
        "aider",
        "Aider",
        translated_providers=frozenset({"openrouter"}),
    )
    registry = Mock()
    registry.get.return_value = current
    config = configured(launcher="aider")

    remediation = LauncherService(registry, config).plan_remediation()

    assert remediation.action_required is False
    assert remediation.current_name == "aider"
    assert remediation.recommended_name == "aider"
    assert remediation.warning is None
    config.update.assert_not_called()
    registry.list.assert_not_called()


def test_apply_remediation_persists_installed_recommendation():
    service, config = remediation_service()

    remediation = service.apply_remediation()

    assert remediation.changed is True
    assert remediation.recommended_name == "aider"
    config.update.assert_called_once_with(launcher="aider")


def test_apply_remediation_refuses_unavailable_recommendation():
    service, config = remediation_service(recommended_installed=False)

    with pytest.raises(RuntimeError, match="not installed"):
        service.apply_remediation()

    config.update.assert_not_called()


def test_remediation_plan_reports_missing_automatic_option():
    current = fake_launcher(
        "claude",
        "Claude Code",
        native_provider="anthropic",
        warning="Potential mismatch",
    )
    registry = Mock()
    registry.get.return_value = current
    registry.list.return_value = [current]

    with pytest.raises(RuntimeError, match="No automatic compatibility remediation"):
        LauncherService(registry, configured()).plan_remediation()
