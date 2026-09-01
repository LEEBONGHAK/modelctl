from dataclasses import dataclass

from sqlalchemy import text

from modelctl_core.launcher.base import LaunchRequest
from modelctl_sdk import LAUNCHER_PLUGIN_CONTRACT_VERSION, is_contract_compatible


@dataclass(frozen=True)
class DiagnosticCheck:
    name: str
    status: str
    detail: str


class DoctorService:
    def __init__(self, config, credentials, providers, launchers, engine):
        self.config = config
        self.credentials = credentials
        self.providers = providers
        self.launchers = launchers
        self.engine = engine

    def run(self) -> list[DiagnosticCheck]:
        config = self.config.load()
        checks = [self._config_check(config)]

        provider_id = config.get("provider")
        model = config.get("default_model")
        launcher_id = config.get("launcher", "claude")

        checks.append(self._provider_check(provider_id))
        checks.append(self._credential_check(provider_id))
        checks.append(self._model_check(model))
        checks.append(self._launcher_check(launcher_id))
        checks.extend(self._plugin_checks(launcher_id))
        checks.append(self._compatibility_check(provider_id, model, launcher_id))
        checks.append(self._database_check())
        return checks

    def _config_check(self, config: dict) -> DiagnosticCheck:
        if self.config.path.exists():
            return DiagnosticCheck("Configuration", "ok", str(self.config.path))
        if config:
            return DiagnosticCheck("Configuration", "ok", "Loaded default configuration")
        return DiagnosticCheck(
            "Configuration",
            "warning",
            f"Not created yet: {self.config.path}",
        )

    def _provider_check(self, provider_id: str | None) -> DiagnosticCheck:
        if not provider_id:
            return DiagnosticCheck("Provider", "error", "Run: modelctl use")

        provider_ids = {provider.id for provider in self.providers.list()}
        if provider_id not in provider_ids:
            return DiagnosticCheck("Provider", "error", f"Unknown provider: {provider_id}")
        return DiagnosticCheck("Provider", "ok", provider_id)

    def _credential_check(self, provider_id: str | None) -> DiagnosticCheck:
        if not provider_id:
            return DiagnosticCheck("Credential", "warning", "Provider is not selected")
        if self.credentials.load(provider_id):
            return DiagnosticCheck("Credential", "ok", f"Credential found for {provider_id}")
        return DiagnosticCheck(
            "Credential",
            "warning",
            f"No credential found for {provider_id}",
        )

    def _model_check(self, model: str | None) -> DiagnosticCheck:
        if not model:
            return DiagnosticCheck("Model", "error", "Run: modelctl use")
        return DiagnosticCheck("Model", "ok", model)

    def _launcher_check(self, launcher_id: str) -> DiagnosticCheck:
        launcher = self.launchers.get(launcher_id)
        if launcher is None:
            return DiagnosticCheck("Launcher", "error", f"Unknown launcher: {launcher_id}")
        if launcher.available():
            return DiagnosticCheck("Launcher", "ok", f"{launcher.display_name} is installed")
        return DiagnosticCheck(
            "Launcher",
            "warning",
            f"{launcher.display_name} is selected but not installed",
        )

    def _plugin_checks(self, selected_launcher_id: str) -> list[DiagnosticCheck]:
        diagnostics = getattr(self.launchers, "diagnostics", None)
        if not callable(diagnostics):
            return []

        checks: list[DiagnosticCheck] = []
        for record in diagnostics():
            if record.source == "builtin:modelctl":
                continue

            name = f"Launcher plugin {record.launcher_id}"
            selected = record.launcher_id == selected_launcher_id

            if record.status != "loaded":
                status = "error" if selected else "warning"
                detail = f"{record.source}; {record.status}"
                if record.error:
                    detail = f"{detail}; {record.error}"
                checks.append(DiagnosticCheck(name, status, detail))
                continue

            launcher = self.launchers.get(record.launcher_id)
            if launcher is None:
                checks.append(
                    DiagnosticCheck(
                        name,
                        "error" if selected else "warning",
                        f"{record.source}; discovery reported loaded but registry entry is missing",
                    )
                )
                continue

            metadata = getattr(launcher, "metadata", None)
            contract_version = getattr(metadata, "contract_version", None)
            plugin_id = record.plugin_id or getattr(metadata, "plugin_id", "unknown")

            try:
                compatible = isinstance(contract_version, str) and is_contract_compatible(
                    contract_version
                )
            except ValueError:
                compatible = False

            if not compatible:
                checks.append(
                    DiagnosticCheck(
                        name,
                        "error" if selected else "warning",
                        f"{record.source}; plugin={plugin_id}; contract={contract_version!r} "
                        f"is incompatible with {LAUNCHER_PLUGIN_CONTRACT_VERSION}",
                    )
                )
                continue

            try:
                available = launcher.available()
            except Exception as error:
                checks.append(
                    DiagnosticCheck(
                        name,
                        "error" if selected else "warning",
                        f"{record.source}; plugin={plugin_id}; "
                        f"contract={contract_version} compatible; availability check failed: "
                        f"{type(error).__name__}: {error}",
                    )
                )
                continue

            checks.append(
                DiagnosticCheck(
                    name,
                    "ok" if available else "warning",
                    f"{record.source}; plugin={plugin_id}; contract={contract_version} "
                    f"compatible; executable={'available' if available else 'unavailable'}",
                )
            )

        return checks

    def _compatibility_check(
        self,
        provider_id: str | None,
        model: str | None,
        launcher_id: str,
    ) -> DiagnosticCheck:
        if not provider_id or not model:
            return DiagnosticCheck(
                "Compatibility",
                "warning",
                "Select a provider and model to evaluate launcher compatibility",
            )

        launcher = self.launchers.get(launcher_id)
        if launcher is None:
            return DiagnosticCheck(
                "Compatibility",
                "warning",
                "Select a known launcher to evaluate compatibility",
            )

        checker = getattr(launcher, "compatibility_warning", None)
        request = LaunchRequest.create(model=model, provider=provider_id)
        warning = checker(request) if callable(checker) else None
        if warning:
            return DiagnosticCheck("Compatibility", "warning", warning)
        return DiagnosticCheck(
            "Compatibility",
            "ok",
            "No known provider/model/launcher compatibility issues",
        )

    def _database_check(self) -> DiagnosticCheck:
        try:
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
        except Exception as exc:
            return DiagnosticCheck("Database", "error", str(exc))
        return DiagnosticCheck("Database", "ok", "Connection succeeded")
