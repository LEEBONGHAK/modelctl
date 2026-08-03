import typer
from rich.console import Console
from rich.table import Table

from modelctl_cli.context import container

launchers_app = typer.Typer(help="Inspect and select coding-agent launchers.")
console = Console()


@launchers_app.command("list")
def list_launchers() -> None:
    """List supported launchers and their local installation status."""
    active = container.config.load().get("launcher", "claude")

    table = Table(title="Coding-agent launchers")
    table.add_column("Active", justify="center")
    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Installed", justify="center")

    for launcher in container.launchers.list():
        table.add_row(
            "✓" if launcher.name == active else "",
            launcher.name,
            launcher.display_name,
            "✓" if launcher.available() else "—",
        )

    console.print(table)


@launchers_app.command("use")
def use_launcher(name: str) -> None:
    """Select the default coding-agent launcher."""
    launcher = container.launchers.get(name)
    if launcher is None:
        supported = ", ".join(item.name for item in container.launchers.list())
        raise typer.BadParameter(
            f"Unknown launcher '{name}'. Expected one of: {supported}"
        )

    container.config.update(launcher=name)
    console.print(f"[green]Selected launcher:[/green] {launcher.display_name}")

    if not launcher.available():
        console.print(
            "[yellow]The launcher is not installed or not available on PATH.[/yellow]"
        )
