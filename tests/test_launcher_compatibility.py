from modelctl_core.launcher.aider import AiderLauncher
from modelctl_core.launcher.base import LaunchRequest
from modelctl_core.launcher.claude import ClaudeCodeLauncher
from modelctl_core.launcher.codex import CodexCliLauncher
from modelctl_core.launcher.gemini import GeminiCliLauncher


def test_native_launchers_warn_for_openrouter_models():
    request = LaunchRequest.create(
        "anthropic/claude-sonnet-4",
        provider="openrouter",
    )

    for launcher in (
        ClaudeCodeLauncher(),
        GeminiCliLauncher(),
        CodexCliLauncher(),
    ):
        warning = launcher.compatibility_warning(request)

        assert warning is not None
        assert launcher.display_name in warning
        assert "modelctl launchers remediate" in warning
        assert "modelctl launchers remediate --apply" in warning


def test_native_launcher_accepts_matching_provider():
    assert (
        ClaudeCodeLauncher().compatibility_warning(
            LaunchRequest.create("sonnet", provider="anthropic")
        )
        is None
    )
    assert (
        GeminiCliLauncher().compatibility_warning(
            LaunchRequest.create("gemini-2.5-pro", provider="google")
        )
        is None
    )
    assert (
        CodexCliLauncher().compatibility_warning(
            LaunchRequest.create("gpt-5", provider="openai")
        )
        is None
    )


def test_aider_accepts_openrouter_provider():
    request = LaunchRequest.create(
        "anthropic/claude-sonnet-4",
        provider="openrouter",
    )

    assert AiderLauncher().compatibility_warning(request) is None
