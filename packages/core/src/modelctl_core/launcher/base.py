from abc import ABC, abstractmethod

from modelctl_core.plugins.metadata import (
    PluginMetadata,
)


class LauncherPlugin(ABC):
    metadata: PluginMetadata

    @abstractmethod
    def detect(self) -> bool:
        ...

    @abstractmethod
    def launch(self):
        ...
