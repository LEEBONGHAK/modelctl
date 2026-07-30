import typer

models_app = typer.Typer()


@models_app.command()
def sync():
    """
    Synchronize models from provider.
    """

    print("Not implemented")


@models_app.command("list")
def list_models():
    """
    List cached models.
    """

    print("Not implemented")