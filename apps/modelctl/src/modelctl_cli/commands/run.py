import typer
from rich.console import Console

from modelctl_cli.context import container

console = Console()


def run() -> None:
    """Launch the configured coding agent with the selected model."""
    console.print("🚀 Starting launcher...")

    try:
        container.launcher_service().run()
    except Exception as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
