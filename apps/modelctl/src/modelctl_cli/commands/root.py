import typer
from rich.console import Console

console = Console()


def register_root_commands(app: typer.Typer):

    @app.command()
    def version():
        console.print("modelctl 0.1.0")

    @app.command()
    def init():
        console.print("🚀 modelctl initialized")

    @app.command()
    def doctor():
        console.print("Checking environment...")
