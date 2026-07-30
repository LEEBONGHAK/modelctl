import getpass

import typer
from rich.console import Console

from modelctl import __version__

from modelctl.core.config import (
    ModelctlConfig,
    save_config,
)

from modelctl.core.database import (
    init_database,
)

from modelctl.registry import (
    get_provider,
)

from modelctl.services.credential import (
    set_secret,
)

from modelctl.services.model_service import (
    get_models,
    save_models,
)


app = typer.Typer(
    name="modelctl",
    help="Universal AI model and coding agent control plane",
)


console = Console()


@app.command()
def version():
    """
    Show version.
    """

    console.print(
        f"modelctl {__version__}"
    )


@app.command()
def init():
    """
    Initialize modelctl environment.
    """

    save_config(
        ModelctlConfig()
    )

    init_database()

    console.print(
        "✅ modelctl initialized"
    )


@app.command()
def doctor():
    """
    Check environment.
    """

    console.print(
        "🩺 Running diagnostics..."
    )


@app.command()
def login(
    provider: str,
):

    """
    Login provider.
    """

    instance = get_provider(provider)

    if instance is None:
        console.print(f"❌ Unknown provider: {provider}")
        raise typer.Exit(code=1)

    instance.login()
    console.print(f"✅ {provider} login successful")    


@app.command()
def refresh():

    """
    Refresh models from providers.
    """

    provider = get_provider(
        "openrouter"
    )

    if provider is None:

        console.print(
            "❌ Provider not found"
        )

        raise typer.Exit(
            code=1
        )


    models = provider.list_models()


    save_models(
        "openrouter",
        models,
    )


    console.print(
        f"✅ {len(models)} models updated"
    )


@app.command()
def providers():

    """
    List providers.
    """

    console.print(
        "openrouter"
    )


@app.command()
def models():

    """
    List models.
    """

    models = get_models()


    if not models:

        console.print(
            "No models available."
        )

        return


    for model in models:

        console.print(
            f"{model.provider:<12}"
            f"{model.model_id}"
        )


@app.command()
def run():

    """
    Launch AI coding agent.
    """

    console.print(
        "Launching..."
    )
