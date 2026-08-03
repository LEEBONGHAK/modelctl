from modelctl_core.config.manager import ConfigManager
from modelctl_core.services.config_service import ConfigService


def test_config_service_updates_runtime_defaults(tmp_path):
    manager = ConfigManager(tmp_path / "config.json")
    service = ConfigService(manager)

    service.set_provider("openrouter")
    service.set_launcher("gemini")
    service.set_model("auto")

    assert service.get() == {
        "provider": "openrouter",
        "launcher": "gemini",
        "default_model": "auto",
    }
