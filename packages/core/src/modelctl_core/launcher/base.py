from abc import ABC, abstractmethod


class Launcher(ABC):
    name: str

    display_name: str

    @abstractmethod
    def run(self, model: str) -> None:
        pass
