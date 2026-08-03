from typing import Annotated

import typer
from rich.console import Console

from modelctl_cli.context import container

console = Console()


def use(
    provider: Annotated[
        str | None,
        typer.Option(
            "--provider",
            "-p",
            help="Provider ID for non-interactive selection.",
        ),
    ] = None,
    model: Annotated[
        str | None,
        typer.Option(
            "--model",
            "-m",
            help="Model ID for non-interactive selection.",
        ),
    ] = None,
) -> None:
    """Select and persist the default provider and model."""
    if (provider is None) != (model is None):
        raise typer.BadParameter("Use --provider and --model together.")

    selection = container.selection_service()

    if provider is not None and model is not None:
        try:
            selected_provider, selected_model = selection.validate(provider, model)
        except ValueError as exc:
            raise typer.BadParameter(str(exc)) from exc
    else:
        selected_provider = selection.select_provider()
        if not selected_provider:
            raise typer.Exit()

        selected_model = selection.select_model(selected_provider)
        if not selected_model:
            raise typer.Exit()

    container.config.update_model(selected_provider, selected_model)

    console.print("\n✔ Default model updated\n")
    console.print(f"Provider: {selected_provider}")
    console.print(f"Model: {selected_model}")
