import typer
from rich.console import Console

from modelctl_cli.context import container

console = Console()


def use() -> None:
    """Select and persist the default provider and model."""
    selection = container.selection_service()

    provider = selection.select_provider()
    if not provider:
        raise typer.Exit()

    model = selection.select_model(provider)
    if not model:
        raise typer.Exit()

    container.config.update_model(provider, model)

    console.print("\n✔ Default model updated\n")
    console.print(f"Provider: {provider}")
    console.print(f"Model: {model}")
