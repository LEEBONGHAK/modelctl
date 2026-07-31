import typer
from rich.console import Console
from rich.table import Table

from modelctl_cli.context import container

console = Console()

models_app = typer.Typer()


@models_app.command()
def sync():

    count = container.model_service().sync()

    console.print(f"✔ Synced {count} models")


@models_app.command("list")
def list_models() -> None:

    service = container.model_service()

    models = service.list()

    table = Table(title="Installed Models")

    table.add_column("★", justify="center", no_wrap=True)
    table.add_column("Provider")
    table.add_column("Model")
    table.add_column("Family")
    table.add_column("Context", justify="right")
    table.add_column("Vision", justify="center")
    table.add_column("Reasoning", justify="center")
    table.add_column("Tools", justify="center")
    table.add_column("Prompt ($/1M)")
    table.add_column("Completion ($/1M)")

    for model in models:
        table.add_row(
            "★" if model.favorite else "",
            model.provider,
            model.model_id,
            model.family or "-",
            f"{model.context_length:,}",
            "✓" if model.supports_vision else "",
            "✓" if model.supports_reasoning else "",
            "✓" if model.supports_tools else "",
            f"{model.prompt_price:g}",
            f"{model.completion_price:g}",
        )

    console.print(table)
