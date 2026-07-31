import typer

from modelctl_cli.context import container


models_app = typer.Typer()


@models_app.command()
def sync():

    count = container.model_service().sync()

    console.print(f"✔ Synced {count} models")
