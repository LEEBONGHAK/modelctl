from functools import cached_property

from modelctl_core.auth.service import CredentialService
from modelctl_core.config.manager import ConfigManager
from modelctl_core.database.engine import get_engine

from modelctl_core.provider.registry import ProviderRegistry

from modelctl_core.repository.model_repository import (
    ModelRepository,
)

from modelctl_core.services.model_service import (
    ModelService,
)


class Container:
    """
    Application Dependency Container

    모든 Core 객체의 생명주기를 관리한다.
    """

    @cached_property
    def config(self):

        return ConfigManager()

    @cached_property
    def engine(self):

        cfg = self.config.load()

        return get_engine(cfg.database_path)

    @cached_property
    def credentials(self):

        return CredentialService()

    @cached_property
    def providers(self):

        registry = ProviderRegistry()

        registry.discover()

        return registry

    @cached_property
    def models(self):

        return ModelRepository(self.engine)

    def model_service(self):

        return ModelService(
            repository=self.models,
            provider_registry=self.providers,
            credentials=self.credentials,
        )
