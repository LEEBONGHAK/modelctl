from functools import cached_property
from pathlib import Path

from modelctl_core.auth.service import CredentialService
from modelctl_core.config.manager import ConfigManager
from modelctl_core.database.engine import get_engine
from modelctl_core.launcher.registry import LauncherRegistry
from modelctl_core.provider.registry import ProviderRegistry
from modelctl_core.repository.model_repository import ModelRepository
from modelctl_core.selector.fzf_selector import FzfSelector
from modelctl_core.services.launcher_service import LauncherService
from modelctl_core.services.model_service import ModelService
from modelctl_core.services.selection_service import SelectionService


class Container:
    """Application dependency container."""

    @cached_property
    def config(self) -> ConfigManager:
        return ConfigManager()

    @cached_property
    def engine(self):
        cfg = self.config.load()
        db_path = cfg.get(
            "database_path",
            str(Path.home() / ".local" / "share" / "modelctl" / "modelctl.db"),
        )
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        return get_engine(db_path)

    @cached_property
    def credentials(self) -> CredentialService:
        return CredentialService()

    @cached_property
    def providers(self) -> ProviderRegistry:
        registry = ProviderRegistry()
        registry.discover()
        return registry

    @cached_property
    def launchers(self) -> LauncherRegistry:
        return LauncherRegistry()

    @cached_property
    def models(self) -> ModelRepository:
        return ModelRepository(self.engine)

    def model_service(self) -> ModelService:
        return ModelService(
            repository=self.models,
            provider_registry=self.providers,
            credentials=self.credentials,
        )

    def selection_service(self) -> SelectionService:
        return SelectionService(
            self.providers,
            self.models,
            FzfSelector(),
        )

    def launcher_service(self) -> LauncherService:
        return LauncherService(
            self.launchers,
            self.config,
        )
