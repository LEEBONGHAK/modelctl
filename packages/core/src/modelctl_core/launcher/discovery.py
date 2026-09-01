from __future__ import annotations

from dataclasses import dataclass
from importlib import metadata as importlib_metadata
from itertools import groupby
from typing import Iterable

from modelctl_sdk import (
    LAUNCHER_ENTRY_POINT_GROUP,
    LauncherCapabilities,
    LauncherMetadata,
    LauncherPlugin,
)

from modelctl_core.launcher.plugin_adapter import PluginLauncherAdapter


@dataclass(frozen=True)
class LauncherDiscoveryRecord:
    launcher_id: str
    source: str
    status: str
    display_name: str | None = None
    plugin_id: str | None = None
    error: str | None = None


def discover_launcher_plugins(
    reserved_ids: set[str],
    entry_points: Iterable[object] | None = None,
) -> tuple[list[PluginLauncherAdapter], list[LauncherDiscoveryRecord]]:
    """Load installed launcher plugins without allowing them to replace built-ins."""

    selected = (
        importlib_metadata.entry_points(group=LAUNCHER_ENTRY_POINT_GROUP)
        if entry_points is None
        else list(entry_points)
    )
    ordered = sorted(selected, key=lambda item: (item.name, item.value, _source(item)))

    launchers: list[PluginLauncherAdapter] = []
    records: list[LauncherDiscoveryRecord] = []

    for launcher_id, grouped in groupby(ordered, key=lambda item: item.name):
        candidates = list(grouped)

        if launcher_id in reserved_ids:
            for entry_point in candidates:
                records.append(
                    LauncherDiscoveryRecord(
                        launcher_id=launcher_id,
                        source=_source(entry_point),
                        status="duplicate",
                        error="Launcher ID conflicts with a built-in launcher.",
                    )
                )
            continue

        if len(candidates) > 1:
            for entry_point in candidates:
                records.append(
                    LauncherDiscoveryRecord(
                        launcher_id=launcher_id,
                        source=_source(entry_point),
                        status="duplicate",
                        error="Multiple installed entry points claim the same launcher ID.",
                    )
                )
            continue

        entry_point = candidates[0]
        source = _source(entry_point)
        try:
            plugin = _load_plugin(entry_point)
            metadata = plugin.metadata
            if metadata.launcher_id != launcher_id:
                raise ValueError(
                    "Entry point name must match plugin metadata launcher_id: "
                    f"{launcher_id!r} != {metadata.launcher_id!r}."
                )
            adapter = PluginLauncherAdapter(plugin)
        except Exception as error:  # plugin import/initialization must be isolated
            records.append(
                LauncherDiscoveryRecord(
                    launcher_id=launcher_id,
                    source=source,
                    status="error",
                    error=f"{type(error).__name__}: {error}",
                )
            )
            continue

        launchers.append(adapter)
        records.append(
            LauncherDiscoveryRecord(
                launcher_id=adapter.name,
                display_name=adapter.display_name,
                plugin_id=metadata.plugin_id,
                source=source,
                status="loaded",
            )
        )

    return launchers, records


def _load_plugin(entry_point) -> LauncherPlugin:
    loaded = entry_point.load()

    if isinstance(loaded, type):
        candidate = loaded()
    elif isinstance(loaded, LauncherPlugin):
        candidate = loaded
    elif callable(loaded):
        candidate = loaded()
    else:
        candidate = loaded

    if not isinstance(candidate, LauncherPlugin):
        raise TypeError(
            "Launcher entry point must expose a LauncherPlugin instance, class, "
            "or zero-argument factory."
        )
    if not isinstance(candidate.metadata, LauncherMetadata):
        raise TypeError("Launcher plugin metadata must be LauncherMetadata.")
    if not isinstance(candidate.capabilities, LauncherCapabilities):
        raise TypeError("Launcher plugin capabilities must be LauncherCapabilities.")

    return candidate


def _source(entry_point) -> str:
    distribution = getattr(entry_point, "dist", None)
    if distribution is None:
        return str(entry_point.value)

    metadata = getattr(distribution, "metadata", None)
    name = metadata.get("Name") if metadata is not None else None
    version = getattr(distribution, "version", None)
    if name and version:
        return f"{name}=={version}"
    if name:
        return str(name)
    return str(entry_point.value)
