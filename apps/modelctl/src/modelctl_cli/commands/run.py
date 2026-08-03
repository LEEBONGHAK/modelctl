from typing import Annotated

import typer
from rich.console import Console

from modelctl_cli.context import container

console = Console()


def run(
    args: Annotated[
        list[str] | None,
        typer.Argument(help="Arguments forwarded to the configured launcher."),
    ] = None,
) -> None:
    """Launch the configured coding agent with the selected model."""
    try:
        service = container.launcher_service()
        warning = service.compatibility_warning()
        if warning:
            console.print(f"[yellow]⚠ Compatibility warning: {warning}[/yellow]")

        console.print("🚀 Starting launcher...")
        service.run(args or [])
    except Exception as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
