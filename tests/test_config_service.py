import pytest

from modelctl_core.config.manager import ConfigManager
from modelctl_core.services.config_service import ConfigService


def test_config_service_updates_runtime_defaults(tmp_path):
    manager = ConfigManager(tmp_path / "config.json")
    service = ConfigService(manager)

    service.set_provider("openrouter")
    service.set_launcher("gemini")
    service.set_model("auto")
    service.set_compatibility_policy("strict")

    assert service.get() == {
        "provider": "openrouter",
        "launcher": "gemini",
        "default_model": "auto",
        "compatibility_policy": "strict",
    }


def test_config_service_normalizes_compatibility_policy(tmp_path):
    service = ConfigService(ConfigManager(tmp_path / "config.json"))

    service.set_compatibility_policy("  WARN  ")

    assert service.get()["compatibility_policy"] == "warn"


def test_config_service_rejects_unknown_compatibility_policy(tmp_path):
    service = ConfigService(ConfigManager(tmp_path / "config.json"))

    with pytest.raises(ValueError, match="Expected one of: strict, warn"):
        service.set_compatibility_policy("automatic")

    assert "compatibility_policy" not in service.get()
