from modelctl_core.config.manager import ConfigManager


class ConfigService:
    def __init__(self, manager: ConfigManager | None = None):
        self.manager = manager or ConfigManager()

    def get(self) -> dict[str, object]:
        return self.manager.load()

    def save(self, config: dict[str, object]) -> None:
        self.manager.save(config)

    def set_provider(self, provider: str) -> None:
        self.manager.update(provider=provider)

    def set_launcher(self, launcher: str) -> None:
        self.manager.update(launcher=launcher)

    def set_model(self, model: str) -> None:
        self.manager.update(default_model=model)
