import typer
from rich.console import Console


app = typer.Typer(
    name="modelctl",
    help="Universal AI model and coding agent control plane",
)

console = Console()

@app.command()
def version():
    console.print(
        "modelctl 0.1.0"
    )



@app.command()
def init():
    console.print(
        "🚀 modelctl initialized"
    )
