from abc import ABC, abstractmethod


class Launcher(ABC):
    name: str
    display_name: str
    native_provider: str | None = None

    def compatibility_warning(self, provider: str | None, model: str) -> str | None:
        """Return a non-blocking warning for a potentially incompatible selection."""
        if not provider or not self.native_provider or provider == self.native_provider:
            return None

        if provider == "openrouter":
            return (
                f"{self.display_name} will receive OpenRouter model '{model}' unchanged. "
                "The native CLI may not recognize that model name or use the OpenRouter "
                "credential automatically. Use `modelctl launchers use aider` for automatic "
                "OpenRouter translation, or configure a model supported by the selected CLI."
            )

        return (
            f"{self.display_name} is designed for provider '{self.native_provider}', but the "
            f"selected provider is '{provider}'. The model will be forwarded unchanged."
        )

    @abstractmethod
    def run(
        self,
        model: str,
        extra_args: list[str] | None = None,
        provider: str | None = None,
    ) -> None:
        """Launch an agent with model, native arguments, and provider context."""
        raise NotImplementedError
