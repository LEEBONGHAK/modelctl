from importlib import metadata

import typer
from rich.console import Console

console = Console()


def installed_version() -> str:
    try:
        return metadata.version("modelctl")
    except metadata.PackageNotFoundError:
        return "unknown"


def register_root_commands(app: typer.Typer):

    @app.command()
    def version():
        console.print(f"modelctl {installed_version()}")

    @app.command()
    def init():
        console.print("🚀 modelctl initialized")

    @app.command()
    def doctor():
        console.print("Checking environment...")
