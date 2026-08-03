import typer
from rich.console import Console

from modelctl_cli.context import container

console = Console()


def run(
    args: list[str] | None = typer.Argument(
        None,
        help="Arguments forwarded to the configured launcher.",
    ),
) -> None:
    """Launch the configured coding agent with the selected model."""
    console.print("🚀 Starting launcher...")

    try:
        container.launcher_service().run(args or [])
    except Exception as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(code=1) from exc
