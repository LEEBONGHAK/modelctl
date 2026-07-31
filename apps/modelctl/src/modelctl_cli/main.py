import typer

from modelctl_cli.commands.root import register_root_commands
from modelctl_cli.commands.config import config_app
from modelctl_cli.commands.plugins import plugins_app
from modelctl_cli.commands.models import models_app
from modelctl_cli.commands.auth import auth_app
from modelctl_cli.commands.use import use_app

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

app.add_typer(
    models_app,
    name="models",
)

app.add_typer(
    auth_app,
    name="auth",
)

app.add_typer(
    use_app,
    name="use",
)

if __name__ == "__main__":
    app()
