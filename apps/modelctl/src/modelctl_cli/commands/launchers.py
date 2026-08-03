from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table
from rich.text import Text

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


@launchers_app.command("recommend")
def recommend_launcher(
    apply: Annotated[
        bool,
        typer.Option(
            "--apply",
            help="Select the recommendation when it is installed and available on PATH.",
        ),
    ] = False,
) -> None:
    """Recommend a launcher for the configured provider and model."""
    service = container.launcher_service()

    try:
        recommendation = (
            service.apply_recommendation() if apply else service.recommend()
        )
    except RuntimeError as error:
        console.print("[red]Launcher recommendation failed:[/red]", Text(str(error)))
        raise typer.Exit(code=1) from error

    if recommendation is None:
        config = container.config.load()
        provider = config.get("provider", "unknown")
        console.print(
            "[yellow]No launcher recommendation is available for provider[/yellow]",
            Text(str(provider)),
        )
        raise typer.Exit(code=1)

    table = Table(title="Launcher recommendation")
    table.add_column("Provider")
    table.add_column("Model")
    table.add_column("Recommended")
    table.add_column("Installed", justify="center")
    table.add_column("Active", justify="center")
    table.add_row(
        Text(recommendation.provider),
        Text(recommendation.model),
        recommendation.display_name,
        "✓" if recommendation.installed else "—",
        "✓" if recommendation.active else "—",
    )
    console.print(table)
    console.print("[bold]Reason:[/bold]", Text(recommendation.reason))

    if apply:
        if recommendation.active:
            console.print("[green]The recommended launcher is already selected.[/green]")
        else:
            console.print(
                "[green]Selected recommended launcher:[/green]",
                recommendation.display_name,
            )


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
