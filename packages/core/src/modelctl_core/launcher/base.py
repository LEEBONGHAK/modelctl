from abc import ABC, abstractmethod

from modelctl_sdk import (
    LAUNCHER_PLUGIN_CONTRACT_VERSION,
    LaunchRequest,
    LauncherCapabilities,
    LauncherMetadata,
)


class Launcher(ABC):
    name: str
    display_name: str
    capabilities = LauncherCapabilities()
    plugin_id = "modelctl.builtin"
    contract_version = LAUNCHER_PLUGIN_CONTRACT_VERSION

    @property
    def metadata(self) -> LauncherMetadata:
        return LauncherMetadata(
            plugin_id=self.plugin_id,
            launcher_id=self.name,
            display_name=self.display_name,
            contract_version=self.contract_version,
        )

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
    def available(self) -> bool:
        """Return whether the launcher executable is available locally."""
        raise NotImplementedError

    @abstractmethod
    def run(self, request: LaunchRequest) -> None:
        """Launch an agent from one immutable execution request."""
        raise NotImplementedError


__all__ = ["LaunchRequest", "Launcher", "LauncherCapabilities", "LauncherMetadata"]
