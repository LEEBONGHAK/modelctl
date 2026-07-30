from abc import ABC, abstractmethod
from modelctl_core.plugins.metadata import (
    PluginMetadata,
)


class Provider(ABC):

    metadata: ProviderMetadata

    @abstractmethod
    def authenticate(
        self,
        credentials,
    ):
        print("1")

    @abstractmethod
    def list_models(self):
        print("1")

    @abstractmethod
    def chat(self):
        print("1")