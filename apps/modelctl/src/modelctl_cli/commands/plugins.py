import typer
from rich.console import Console

from modelctl_core.plugins.registry import (
    PluginRegistry,
)

console = Console()

plugins_app = typer.Typer()


@plugins_app.command("list")
def list_plugins():
    registry = PluginRegistry()
    registry.discover()

    console.print("Installed Plugins")

    console.print("\nProviders:")
    for provider in registry.list_providers():
        console.print(f"  {provider.metadata.name}")

    console.print("\nLaunchers:")
    for launcher in registry.list_launchers():
        console.print(f"  {launcher.metadata.name}")
