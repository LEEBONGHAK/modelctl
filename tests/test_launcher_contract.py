from dataclasses import FrozenInstanceError

import pytest

from modelctl_core.launcher.base import LaunchRequest, LauncherCapabilities


def test_launch_request_copies_native_arguments_into_immutable_tuple():
    extra_args = ["--sandbox", "workspace-write"]

    request = LaunchRequest.create(
        "gpt-5.6",
        provider="openai",
        extra_args=extra_args,
    )
    extra_args.append("--dangerously-bypass-approvals-and-sandbox")

    assert request.extra_args == ("--sandbox", "workspace-write")
    with pytest.raises(FrozenInstanceError):
        request.model = "changed"


def test_launcher_capabilities_distinguish_native_and_translated_providers():
    native = LauncherCapabilities(native_provider="anthropic")
    routed = LauncherCapabilities(
        accepts_any_provider=True,
        translated_providers=frozenset({"openrouter"}),
    )

    assert native.accepts("anthropic") is True
    assert native.accepts("openrouter") is False
    assert routed.accepts("openrouter") is True
    assert routed.translates("openrouter") is True
    assert routed.translates("anthropic") is False
