import typer
from rich.console import Console

from modelctl_core.plugins.registry import (
    PluginRegistry,
)

app = typer.Typer(
    name="modelctl",
    help="Universal AI model and coding agent control plane",
)

console = Console()

@app.command()
def version():
    console.print("modelctl 0.1.0")

@app.command()
def init():
    console.print("🚀 modelctl initialized")


@app.command()
def plugins():
    registry = PluginRegistry()
    registry.discover()

    console.print("Installed Plugins")

    console.print("\nProviders:")
    for provider in registry.list_providers():
        console.print(f"  {provider.metadata.name}")

    console.print("\nLaunchers:")
    for launcher in registry.list_launchers():
        console.print(f"  {launcher.metadata.name}")