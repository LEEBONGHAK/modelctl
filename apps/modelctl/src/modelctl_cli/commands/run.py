from typing import Annotated

import typer
from rich.console import Console

from modelctl_cli.context import container

console = Console()


def run(
    strict_compatibility: Annotated[
        bool | None,
        typer.Option(
            "--strict-compatibility/--warn-compatibility",
            help=(
                "Override the configured compatibility policy for this run. "
                "Without either flag, the persisted policy is used."
            ),
        ),
    ] = None,
    args: Annotated[
        list[str] | None,
        typer.Argument(help="Arguments forwarded to the configured launcher."),
    ] = None,
) -> None:
    """Launch the configured coding agent with the selected model."""
    try:
        service = container.launcher_service()
        policy = None
        if strict_compatibility is not None:
            policy = "strict" if strict_compatibility else "warn"

        warning = service.check_compatibility(policy=policy)
        if warning:
            console.print(f"[yellow]⚠ Compatibility warning: {warning}[/yellow]")

        console.print("🚀 Starting launcher...")
        service.run(args or [])
    except Exception as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
