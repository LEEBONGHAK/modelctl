from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class LauncherCapabilities:
    """Static behavior exposed by a launcher implementation."""

    native_provider: str | None = None
    accepts_any_provider: bool = False
    translated_providers: frozenset[str] = frozenset()

    def accepts(self, provider: str | None) -> bool:
        return (
            provider is None
            or self.accepts_any_provider
            or provider == self.native_provider
        )

    def translates(self, provider: str) -> bool:
        return provider in self.translated_providers


@dataclass(frozen=True)
class LaunchRequest:
    """Validated modelctl input passed to one launcher execution."""

    model: str
    provider: str | None = None
    extra_args: tuple[str, ...] = ()

    @classmethod
    def create(
        cls,
        model: str,
        provider: str | None = None,
        extra_args: list[str] | tuple[str, ...] | None = None,
    ) -> "LaunchRequest":
        return cls(
            model=model,
            provider=provider,
            extra_args=tuple(extra_args or ()),
        )


class Launcher(ABC):
    name: str
    display_name: str
    capabilities = LauncherCapabilities()

    def compatibility_warning(self, request: LaunchRequest) -> str | None:
        """Return a non-blocking warning for a potentially incompatible request."""
        provider = request.provider
        if self.capabilities.accepts(provider):
            return None

        remediation = (
            "Run `modelctl launchers remediate` to inspect a compatible launcher, or "
            "`modelctl launchers remediate --apply` to select an installed recommendation."
        )
        if provider == "openrouter":
            return (
                f"{self.display_name} will receive OpenRouter model '{request.model}' "
                "unchanged. The native CLI may not recognize that model name or use the "
                f"OpenRouter credential automatically. {remediation}"
            )

        return (
            f"{self.display_name} is designed for provider "
            f"'{self.capabilities.native_provider}', but the selected provider is "
            f"'{provider}'. The model will be forwarded unchanged. {remediation}"
        )

    @abstractmethod
    def run(self, request: LaunchRequest) -> None:
        """Launch an agent from one immutable execution request."""
        raise NotImplementedError
