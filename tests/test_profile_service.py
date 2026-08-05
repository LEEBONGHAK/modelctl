from types import SimpleNamespace

import pytest

from modelctl_core.config.manager import ConfigManager
from modelctl_core.services.profile_service import ProfileService


class SelectionValidator:
    def __init__(self, error: ValueError | None = None):
        self.error = error
        self.calls: list[tuple[str, str]] = []

    def validate(self, provider: str, model: str) -> tuple[str, str]:
        self.calls.append((provider, model))
        if self.error is not None:
            raise self.error
        return provider, model


class LauncherRegistry:
    def __init__(self, *names: str):
        self.launchers = {name: SimpleNamespace(name=name) for name in names}

    def get(self, name: str):
        return self.launchers.get(name)

    def list(self):
        return list(self.launchers.values())


def service(tmp_path, *, selection=None, launchers=None):
    manager = ConfigManager(tmp_path / "config.json")
    return (
        ProfileService(
            manager,
            selection or SelectionValidator(),
            launchers or LauncherRegistry("claude", "aider"),
        ),
        manager,
    )


def test_save_snapshots_effective_defaults_and_normalizes_name(tmp_path):
    profile_service, manager = service(tmp_path)
    manager.save(
        {
            "provider": "openrouter",
            "default_model": "anthropic/claude-sonnet-4",
        }
    )

    profile = profile_service.save("  WORK  ")

    assert profile.name == "work"
    assert profile.launcher == "claude"
    assert profile.compatibility_policy == "warn"
    assert manager.load()["profiles"] == {
        "work": {
            "provider": "openrouter",
            "default_model": "anthropic/claude-sonnet-4",
            "launcher": "claude",
            "compatibility_policy": "warn",
        }
    }


def test_save_replaces_an_existing_normalized_profile(tmp_path):
    profile_service, manager = service(tmp_path)
    manager.save(
        {
            "provider": "openrouter",
            "default_model": "first/model",
            "launcher": "aider",
            "compatibility_policy": "strict",
        }
    )
    profile_service.save("work")
    manager.update(default_model="second/model")

    profile_service.save("WORK")

    assert manager.load()["profiles"]["work"]["default_model"] == "second/model"


def test_use_validates_then_atomically_applies_profile(tmp_path):
    selection = SelectionValidator()
    profile_service, manager = service(tmp_path, selection=selection)
    manager.save(
        {
            "provider": "openai",
            "default_model": "gpt-5.6",
            "launcher": "claude",
            "compatibility_policy": "warn",
            "database_path": "/tmp/modelctl.db",
            "profiles": {
                "work": {
                    "provider": "openrouter",
                    "default_model": "anthropic/claude-sonnet-4",
                    "launcher": "aider",
                    "compatibility_policy": "strict",
                }
            },
        }
    )

    profile = profile_service.use("work")

    assert selection.calls == [("openrouter", "anthropic/claude-sonnet-4")]
    assert profile.launcher == "aider"
    assert manager.load() == {
        "provider": "openrouter",
        "default_model": "anthropic/claude-sonnet-4",
        "launcher": "aider",
        "compatibility_policy": "strict",
        "database_path": "/tmp/modelctl.db",
        "profiles": {
            "work": {
                "provider": "openrouter",
                "default_model": "anthropic/claude-sonnet-4",
                "launcher": "aider",
                "compatibility_policy": "strict",
            }
        },
    }


def test_use_does_not_mutate_config_when_model_validation_fails(tmp_path):
    selection = SelectionValidator(ValueError("Unknown model for openrouter: missing"))
    profile_service, manager = service(tmp_path, selection=selection)
    original = {
        "provider": "openai",
        "default_model": "gpt-5.6",
        "profiles": {
            "broken": {
                "provider": "openrouter",
                "default_model": "missing",
                "launcher": "aider",
                "compatibility_policy": "strict",
            }
        },
    }
    manager.save(original)

    with pytest.raises(ValueError, match="Unknown model"):
        profile_service.use("broken")

    assert manager.load() == original


def test_use_does_not_mutate_config_for_unknown_launcher(tmp_path):
    profile_service, manager = service(tmp_path)
    original = {
        "provider": "openai",
        "default_model": "gpt-5.6",
        "profiles": {
            "broken": {
                "provider": "openrouter",
                "default_model": "anthropic/claude-sonnet-4",
                "launcher": "unknown",
                "compatibility_policy": "strict",
            }
        },
    }
    manager.save(original)

    with pytest.raises(ValueError, match="Unknown launcher"):
        profile_service.use("broken")

    assert manager.load() == original


def test_delete_removes_last_profile_and_refuses_unknown_names(tmp_path):
    profile_service, manager = service(tmp_path)
    manager.save(
        {
            "provider": "openrouter",
            "default_model": "anthropic/claude-sonnet-4",
            "profiles": {
                "work": {
                    "provider": "openrouter",
                    "default_model": "anthropic/claude-sonnet-4",
                    "launcher": "aider",
                    "compatibility_policy": "strict",
                }
            },
        }
    )

    deleted = profile_service.delete("work")

    assert deleted.name == "work"
    assert "profiles" not in manager.load()
    with pytest.raises(ValueError, match="Unknown profile: work"):
        profile_service.delete("work")


def test_rejects_invalid_names_and_malformed_stored_profiles(tmp_path):
    profile_service, manager = service(tmp_path)

    with pytest.raises(ValueError, match="Invalid profile name"):
        profile_service.get("bad profile")

    manager.save(
        {
            "profiles": {
                "broken": {
                    "provider": "openrouter",
                    "default_model": "model",
                    "launcher": "aider",
                    "compatibility_policy": "strict",
                    "api_key": "must-not-be-accepted",
                }
            }
        }
    )
    with pytest.raises(ValueError, match="unexpected api_key"):
        profile_service.list()
