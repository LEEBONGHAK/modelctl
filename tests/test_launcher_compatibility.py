from modelctl_core.launcher.aider import AiderLauncher
from modelctl_core.launcher.claude import ClaudeCodeLauncher
from modelctl_core.launcher.codex import CodexCliLauncher
from modelctl_core.launcher.gemini import GeminiCliLauncher


def test_native_launchers_warn_for_openrouter_models():
    model = "anthropic/claude-sonnet-4"

    for launcher in (
        ClaudeCodeLauncher(),
        GeminiCliLauncher(),
        CodexCliLauncher(),
    ):
        warning = launcher.compatibility_warning("openrouter", model)

        assert warning is not None
        assert launcher.display_name in warning
        assert "modelctl launchers use aider" in warning


def test_native_launcher_accepts_matching_provider():
    assert ClaudeCodeLauncher().compatibility_warning("anthropic", "sonnet") is None
    assert GeminiCliLauncher().compatibility_warning("google", "gemini-2.5-pro") is None
    assert CodexCliLauncher().compatibility_warning("openai", "gpt-5") is None


def test_aider_accepts_openrouter_provider():
    assert (
        AiderLauncher().compatibility_warning(
            "openrouter",
            "anthropic/claude-sonnet-4",
        )
        is None
    )
