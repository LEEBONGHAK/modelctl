from typing import Optional

import typer
from rich.console import Console

from modelctl import __version__


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


@app.command()
def doctor():
    """
    Check environment.
    """

    console.print(
        "🩺 Running diagnostics..."
    )


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
