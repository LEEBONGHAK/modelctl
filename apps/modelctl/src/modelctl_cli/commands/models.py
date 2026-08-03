import typer
from rich.console import Console
from rich.table import Table

from modelctl_cli.context import container

models_app = typer.Typer(help="Synchronize and inspect provider model catalogs.")
console = Console()


@models_app.command()
def sync(provider: str = "openrouter") -> None:
    """Synchronize models from a configured provider."""
    try:
        count = container.model_service().sync(provider)
    except (ValueError, RuntimeError) as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(code=1) from error

    console.print(f"✔ synced {count} models")


@models_app.command("list")
def list_models() -> None:
    models = container.model_service().list()

    table = Table(title="Models")
    table.add_column("★")
    table.add_column("Provider")
    table.add_column("Model")
    table.add_column("Context")

    for model in models:
        table.add_row(
            "★" if model.favorite else "",
            model.provider,
            model.model_id,
            str(model.context_length),
        )

    console.print(table)


@models_app.command()
def favorite(action: str, model_id: str) -> None:
    service = container.model_service()

    if action == "add":
        service.favorite(model_id, True)
    elif action == "remove":
        service.favorite(model_id, False)
    else:
        raise typer.BadParameter("Action must be 'add' or 'remove'.")

    console.print("updated")
