from abc import ABC, abstractmethod

from modelctl_core.auth.types import Credential
from modelctl_core.plugins.metadata import (
    PluginMetadata,
)


class Provider(ABC):
    id: str
    display_name: str
    metadata: ProviderMetadata

    @abstractmethod
    def authenticate(
        self,
        credentials,
    ):
        print("1")

    @abstractmethod
    def list_models(self, credential: Credential):
        print("1")

    @abstractmethod
    def chat(self):
        print("1")
