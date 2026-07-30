from abc import ABC, abstractmethod
from modelctl_core.plugins.metadata import (
    PluginMetadata,
)

class ProviderPlugin(ABC):
    metadata: PluginMetadata

    @abstractmethod
    def validate(self) -> bool:
        ...

    @abstractmethod
    def list_models(self):
        ...
