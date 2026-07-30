import typer

from modelctl_cli.commands.root import register_root_commands
from modelctl_cli.commands.config import config_app
from modelctl_cli.commands.plugins import plugins_app

app = typer.Typer(
    name="modelctl",
    help="Universal AI model and coding agent control plane",
)

register_root_commands(app)

app.add_typer(
    config_app,
    name="config",
)

app.add_typer(
    plugins_app,
    name="plugins",
)

if __name__ == "__main__":
    app()
