from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from modelctl_core.launcher.base import LaunchRequest
from modelctl_core.launcher.registry import LauncherRegistry
from modelctl_core.services.launcher_service import LauncherService
from modelctl_sdk import LauncherCapabilities, LauncherMetadata


class FakeEntryPoint:
    def __init__(
        self,
        name,
        target,
        *,
        value=None,
        package="test-plugin",
        version="1.0.0",
    ):
        self.name = name
        self.value = value or f"test_plugin:{name}"
        self._target = target
        self.load = Mock(side_effect=self._load)
        self.dist = SimpleNamespace(
            metadata={"Name": package},
            version=version,
        )

    def _load(self):
        if isinstance(self._target, BaseException):
            raise self._target
        return self._target


class CustomLauncher:
    metadata = LauncherMetadata(
        plugin_id="example.plugin",
        launcher_id="custom",
        display_name="Custom Launcher",
    )
    capabilities = LauncherCapabilities(native_provider="custom-provider")

    def __init__(self):
        self.requests = []

    def available(self):
        return True

    def run(self, request):
        self.requests.append(request)


class OtherLauncher:
    metadata = LauncherMetadata(
        plugin_id="example.other",
        launcher_id="other",
        display_name="Other Launcher",
    )
    capabilities = LauncherCapabilities(native_provider="other-provider")

    def available(self):
        return False

    def run(self, request):
        return None


def test_registry_discovers_installed_plugin_and_preserves_runtime_semantics():
    entry_point = FakeEntryPoint("custom", CustomLauncher, package="modelctl-custom")
    registry = LauncherRegistry(entry_points=[entry_point])

    launcher = registry.get("custom")
    assert launcher is not None
    assert launcher.display_name == "Custom Launcher"
    assert launcher.capabilities.native_provider == "custom-provider"
    assert launcher.available() is True

    request = LaunchRequest.create("custom-model", provider="custom-provider")
    launcher.run(request)
    assert launcher._plugin.requests == [request]

    record = next(item for item in registry.diagnostics() if item.launcher_id == "custom")
    assert record.status == "loaded"
    assert record.source == "modelctl-custom==1.0.0"
    assert record.plugin_id == "example.plugin"


def test_builtin_launcher_id_collision_is_rejected_without_loading_plugin():
    entry_point = FakeEntryPoint("claude", CustomLauncher)
    registry = LauncherRegistry(entry_points=[entry_point])

    assert registry.get("claude").plugin_id == "modelctl.builtin"
    entry_point.load.assert_not_called()
    record = registry.diagnostics()[-1]
    assert record.status == "duplicate"
    assert "built-in" in record.error


def test_duplicate_external_launcher_ids_are_all_rejected_deterministically():
    first = FakeEntryPoint("custom", CustomLauncher, value="a:first", package="plugin-a")
    second = FakeEntryPoint("custom", CustomLauncher, value="b:second", package="plugin-b")
    registry = LauncherRegistry(entry_points=[second, first])

    assert registry.get("custom") is None
    first.load.assert_not_called()
    second.load.assert_not_called()
    duplicates = [
        item for item in registry.diagnostics() if item.launcher_id == "custom"
    ]
    assert len(duplicates) == 2
    assert all(item.status == "duplicate" for item in duplicates)
    assert [item.source for item in duplicates] == [
        "plugin-a==1.0.0",
        "plugin-b==1.0.0",
    ]


def test_broken_plugin_is_isolated_while_other_plugin_loads():
    broken = FakeEntryPoint("broken", ImportError("boom"), package="broken-plugin")
    working = FakeEntryPoint("other", OtherLauncher, package="working-plugin")
    registry = LauncherRegistry(entry_points=[broken, working])

    assert registry.get("broken") is None
    assert registry.get("other") is not None
    records = {item.launcher_id: item for item in registry.diagnostics()}
    assert records["broken"].status == "error"
    assert "ImportError: boom" in records["broken"].error
    assert records["other"].status == "loaded"


def test_entry_point_name_must_match_launcher_metadata_id():
    entry_point = FakeEntryPoint("alias", CustomLauncher)
    registry = LauncherRegistry(entry_points=[entry_point])

    assert registry.get("alias") is None
    record = registry.diagnostics()[-1]
    assert record.status == "error"
    assert "must match" in record.error


def test_incompatible_contract_failure_is_visible_and_isolated():
    class IncompatibleLauncher:
        def __init__(self):
            self.metadata = LauncherMetadata(
                plugin_id="example.incompatible",
                launcher_id="incompatible",
                display_name="Incompatible",
                contract_version="2.0",
            )

    entry_point = FakeEntryPoint("incompatible", IncompatibleLauncher)
    registry = LauncherRegistry(entry_points=[entry_point])

    assert registry.get("incompatible") is None
    record = registry.diagnostics()[-1]
    assert record.status == "error"
    assert "Incompatible launcher plugin contract version" in record.error


def test_discovered_plugin_participates_in_launcher_recommendation():
    entry_point = FakeEntryPoint("custom", CustomLauncher)
    registry = LauncherRegistry(entry_points=[entry_point])
    config = Mock()
    config.load.return_value = {
        "provider": "custom-provider",
        "default_model": "custom-model",
        "launcher": "claude",
    }
    service = LauncherService(registry, config)

    recommendation = service.recommend()

    assert recommendation is not None
    assert recommendation.name == "custom"
    assert recommendation.display_name == "Custom Launcher"
    assert recommendation.installed is True


def test_discovered_plugin_participates_in_remediation_and_strict_compatibility():
    entry_point = FakeEntryPoint("custom", CustomLauncher)
    registry = LauncherRegistry(entry_points=[entry_point])
    config = Mock()
    config.load.return_value = {
        "provider": "custom-provider",
        "default_model": "custom-model",
        "launcher": "claude",
    }
    service = LauncherService(registry, config)

    remediation = service.plan_remediation()

    assert remediation.action_required is True
    assert remediation.current_name == "claude"
    assert remediation.recommended_name == "custom"
    assert remediation.recommended_installed is True

    config.load.return_value = {
        "provider": "custom-provider",
        "default_model": "custom-model",
        "launcher": "custom",
    }
    assert service.check_compatibility(policy="strict") is None


def test_discovered_plugin_receives_forwarded_arguments_as_immutable_request():
    entry_point = FakeEntryPoint("custom", CustomLauncher)
    registry = LauncherRegistry(entry_points=[entry_point])
    config = Mock()
    config.load.return_value = {
        "provider": "custom-provider",
        "default_model": "custom-model",
        "launcher": "custom",
    }
    service = LauncherService(registry, config)

    service.run(extra_args=["--mode", "fast"])

    launcher = registry.get("custom")
    assert launcher is not None
    assert launcher._plugin.requests == [
        LaunchRequest(
            model="custom-model",
            provider="custom-provider",
            extra_args=("--mode", "fast"),
        )
    ]


def test_unavailable_discovered_plugin_cannot_be_applied_as_recommendation():
    entry_point = FakeEntryPoint("other", OtherLauncher)
    registry = LauncherRegistry(entry_points=[entry_point])
    config = Mock()
    config.load.return_value = {
        "provider": "other-provider",
        "default_model": "other-model",
        "launcher": "claude",
    }
    service = LauncherService(registry, config)

    recommendation = service.recommend()
    assert recommendation is not None
    assert recommendation.name == "other"
    assert recommendation.installed is False

    with pytest.raises(RuntimeError, match="not installed"):
        service.apply_recommendation()

    config.update.assert_not_called()
