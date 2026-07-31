import typer
from rich.console import Console

from modelctl_cli.context import container

run_app = typer.Typer()
console = Console()


@run_app.command()
def run():
    console.print("🚀 Starting launcher...")

    try:
        container.launcher_service().run()
    except Exception as e:
        console.print(f"[red]{e}[/red]")
        raise typer.Exit(code=1)
