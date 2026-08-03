import json

import typer

from modelctl_core.services.config_service import ConfigService

config_app = typer.Typer(help="Inspect and update modelctl defaults.")


@config_app.command("show")
def show() -> None:
    """Show the current modelctl configuration."""
    typer.echo(json.dumps(ConfigService().get(), indent=2))


@config_app.command("set")
def set_value(key: str, value: str) -> None:
    """Set provider, launcher, or model defaults."""
    service = ConfigService()
    setters = {
        "provider": service.set_provider,
        "launcher": service.set_launcher,
        "model": service.set_model,
    }

    setter = setters.get(key)
    if setter is None:
        raise typer.BadParameter(
            f"Unknown key '{key}'. Expected one of: provider, launcher, model"
        )

    setter(value)
    typer.echo(f"Set {key} to {value}")
