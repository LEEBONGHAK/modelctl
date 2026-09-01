from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass
from typing import Protocol, TypeAlias, runtime_checkable

LAUNCHER_PLUGIN_CONTRACT_VERSION = "1.0"
LAUNCHER_ENTRY_POINT_GROUP = "modelctl.launchers"
_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]{0,63}$")


def contract_major(version: str) -> int:
    try:
        major, minor = version.split(".", 1)
        if not major.isdigit() or not minor.isdigit():
            raise ValueError
        return int(major)
    except ValueError as error:
        raise ValueError(
            f"Invalid launcher plugin contract version: {version!r}. Expected '<major>.<minor>'."
        ) from error


def is_contract_compatible(version: str) -> bool:
    return contract_major(version) == contract_major(LAUNCHER_PLUGIN_CONTRACT_VERSION)


def require_compatible_contract(version: str) -> None:
    if not is_contract_compatible(version):
        raise ValueError(
            "Incompatible launcher plugin contract version "
            f"{version!r}; modelctl supports {LAUNCHER_PLUGIN_CONTRACT_VERSION!r}."
        )


@dataclass(frozen=True)
class LauncherMetadata:
    plugin_id: str
    launcher_id: str
    display_name: str
    contract_version: str = LAUNCHER_PLUGIN_CONTRACT_VERSION

    def __post_init__(self) -> None:
        for label, value in (("plugin_id", self.plugin_id), ("launcher_id", self.launcher_id)):
            if _ID_PATTERN.fullmatch(value) is None:
                raise ValueError(
                    f"Invalid {label} {value!r}. Use 1-64 lowercase letters, numbers, dots, "
                    "underscores, or hyphens, beginning with a letter or number."
                )
        if not self.display_name.strip():
            raise ValueError("Launcher display_name must be a non-empty string.")
        require_compatible_contract(self.contract_version)


@dataclass(frozen=True)
class LauncherCapabilities:
    native_provider: str | None = None
    accepts_any_provider: bool = False
    translated_providers: frozenset[str] = frozenset()

    def accepts(self, provider: str | None) -> bool:
        return provider is None or self.accepts_any_provider or provider == self.native_provider

    def translates(self, provider: str) -> bool:
        return provider in self.translated_providers


@dataclass(frozen=True)
class LaunchRequest:
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
        return cls(model=model, provider=provider, extra_args=tuple(extra_args or ()))


@runtime_checkable
class LauncherPlugin(Protocol):
    @property
    def metadata(self) -> LauncherMetadata: ...

    @property
    def capabilities(self) -> LauncherCapabilities: ...

    def available(self) -> bool: ...

    def run(self, request: LaunchRequest) -> None: ...


LauncherPluginFactory: TypeAlias = Callable[[], LauncherPlugin]
