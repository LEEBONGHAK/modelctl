import typer

from modelctl_cli.context import container


models_app = typer.Typer()


@models_app.command()
def sync():

    service = container.model_service()

    count = service.sync()

    typer.echo(
        f"Synced {count} models"
    )