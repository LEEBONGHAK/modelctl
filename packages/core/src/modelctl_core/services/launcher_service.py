class LauncherService:
    def __init__(self, registry, config):
        self.registry = registry
        self.config = config

    def run(self, extra_args: list[str] | None = None) -> None:
        config = self.config.load()
        launcher_name = config.get("launcher", "claude")
        model = config.get("default_model")

        if not model:
            raise RuntimeError("No model selected. Run: modelctl use")

        launcher = self.registry.get(launcher_name)

        if not launcher:
            raise RuntimeError(f"Unknown launcher: {launcher_name}")

        launcher.run(model, extra_args)
