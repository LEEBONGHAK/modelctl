from modelctl_core.config.manager import ConfigManager


COMPATIBILITY_POLICIES = frozenset({"warn", "strict"})


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

    def set_compatibility_policy(self, policy: str) -> None:
        normalized = policy.strip().lower()
        if normalized not in COMPATIBILITY_POLICIES:
            expected = ", ".join(sorted(COMPATIBILITY_POLICIES))
            raise ValueError(
                f"Unknown compatibility policy '{policy}'. Expected one of: {expected}"
            )
        self.manager.update(compatibility_policy=normalized)
