import typer

from modelctl_cli.commands.auth import auth_app
from modelctl_cli.commands.config import config_app
from modelctl_cli.commands.doctor import doctor
from modelctl_cli.commands.launchers import launchers_app
from modelctl_cli.commands.models import models_app
from modelctl_cli.commands.plugins import plugins_app
from modelctl_cli.commands.root import register_root_commands
from modelctl_cli.commands.run import run
from modelctl_cli.commands.use import use

app = typer.Typer(
    name="modelctl",
    help="Universal AI model and coding agent control plane",
)

register_root_commands(app)

app.add_typer(config_app, name="config")
app.add_typer(launchers_app, name="launchers")
app.add_typer(plugins_app, name="plugins")
app.add_typer(models_app, name="models")
app.add_typer(auth_app, name="auth")

app.command("use")(use)
app.command(
    "run",
    context_settings={
        "allow_extra_args": True,
        "ignore_unknown_options": True,
    },
)(run)
app.command("doctor")(doctor)

if __name__ == "__main__":
    app()
