from typing import Optional

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

from modelctl.commands.doctor import run_doctor

app = typer.Typer(
    name="modelctl",
    help="Universal AI model and coding agent control plane",
)


console = Console()


@app.callback()
def main():
    """
    modelctl CLI
    """
    pass


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

    console.print(
        "🚀 Initializing modelctl..."
    )

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

    run_doctor(console)

@app.command()
def providers():
    """
    List available providers.
    """

    console.print(
        "No providers installed."
    )


@app.command()
def models():
    """
    List available models.
    """

    console.print(
        "No models available."
    )


@app.command()
def run():
    """
    Launch AI coding agent.
    """

    console.print(
        "Launching..."
    )
