"""Public SDK for building modelctl launcher plugins."""

from modelctl_sdk.launcher import (
    LAUNCHER_PLUGIN_CONTRACT_VERSION,
    LaunchRequest,
    LauncherCapabilities,
    LauncherMetadata,
    LauncherPlugin,
    contract_major,
    is_contract_compatible,
    require_compatible_contract,
)

__version__ = "0.3.0"

__all__ = [
    "LAUNCHER_PLUGIN_CONTRACT_VERSION",
    "LaunchRequest",
    "LauncherCapabilities",
    "LauncherMetadata",
    "LauncherPlugin",
    "contract_major",
    "is_contract_compatible",
    "require_compatible_contract",
]
