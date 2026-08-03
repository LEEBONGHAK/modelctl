class LauncherService:
    def __init__(self, registry, config):
        self.registry = registry
        self.config = config

    def compatibility_warning(self) -> str | None:
        launcher, model, provider = self._selection()
        return launcher.compatibility_warning(provider, model)

    def run(self, extra_args: list[str] | None = None) -> None:
        launcher, model, provider = self._selection()
        launcher.run(
            model,
            extra_args,
            provider=provider,
        )

    def _selection(self):
        config = self.config.load()
        launcher_name = config.get("launcher", "claude")
        model = config.get("default_model")
        provider = config.get("provider")

        if not isinstance(model, str) or not model:
            raise RuntimeError("No model selected. Run: modelctl use")

        launcher = self.registry.get(launcher_name)
        if not launcher:
            raise RuntimeError(f"Unknown launcher: {launcher_name}")

        return (
            launcher,
            model,
            provider if isinstance(provider, str) else None,
        )
