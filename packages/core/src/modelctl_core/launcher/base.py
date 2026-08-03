from abc import ABC, abstractmethod


class Launcher(ABC):
    name: str
    display_name: str

    @abstractmethod
    def run(
        self,
        model: str,
        extra_args: list[str] | None = None,
        provider: str | None = None,
    ) -> None:
        """Launch an agent with model, native arguments, and provider context."""
        raise NotImplementedError
