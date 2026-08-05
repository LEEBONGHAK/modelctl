from dataclasses import FrozenInstanceError

import pytest

from modelctl_core.launcher.registry import LauncherRegistry
from modelctl_sdk import (
    LAUNCHER_PLUGIN_CONTRACT_VERSION,
    LaunchRequest,
    LauncherCapabilities,
    LauncherMetadata,
    LauncherPlugin,
    is_contract_compatible,
    require_compatible_contract,
)


def test_sdk_launch_request_is_immutable_and_copies_arguments():
    arguments = ["--sandbox", "workspace-write"]
    request = LaunchRequest.create("gpt-5.6", provider="openai", extra_args=arguments)
    arguments.append("--dangerously-bypass-approvals-and-sandbox")

    assert request.extra_args == ("--sandbox", "workspace-write")
    with pytest.raises(FrozenInstanceError):
        request.model = "changed"


def test_sdk_capabilities_preserve_existing_provider_semantics():
    capabilities = LauncherCapabilities(
        accepts_any_provider=True,
        translated_providers=frozenset({"openrouter"}),
    )

    assert capabilities.accepts("openai") is True
    assert capabilities.translates("openrouter") is True
    assert capabilities.translates("anthropic") is False


def test_launcher_metadata_validates_ids_and_contract_version():
    metadata = LauncherMetadata(
        plugin_id="example.launchers",
        launcher_id="example-cli",
        display_name="Example CLI",
    )

    assert metadata.contract_version == LAUNCHER_PLUGIN_CONTRACT_VERSION

    with pytest.raises(ValueError, match="Invalid launcher_id"):
        LauncherMetadata("example.launchers", "Example CLI", "Example CLI")
    with pytest.raises(ValueError, match="Incompatible"):
        LauncherMetadata(
            "example.launchers",
            "example",
            "Example CLI",
            contract_version="2.0",
        )


def test_contract_compatibility_accepts_same_major_only():
    assert is_contract_compatible("1.9") is True
    assert is_contract_compatible("2.0") is False
    require_compatible_contract("1.1")

    with pytest.raises(ValueError, match="Expected '<major>.<minor>'"):
        is_contract_compatible("latest")


def test_all_builtin_launchers_satisfy_public_plugin_contract():
    launchers = LauncherRegistry().list()

    assert launchers
    for launcher in launchers:
        assert isinstance(launcher, LauncherPlugin)
        assert launcher.metadata.plugin_id == "modelctl.builtin"
        assert launcher.metadata.launcher_id == launcher.name
        assert launcher.metadata.display_name == launcher.display_name
        assert launcher.metadata.contract_version == LAUNCHER_PLUGIN_CONTRACT_VERSION
