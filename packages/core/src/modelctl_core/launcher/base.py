from abc import ABC, abstractmethod


class Launcher(ABC):
    name: str
    display_name: str

    @abstractmethod
    def run(self, model: str, extra_args: list[str] | None = None) -> None:
        """Launch an agent with the selected model and optional native CLI arguments."""
        raise NotImplementedError
