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
    """Set provider, launcher, model, or compatibility defaults."""
    service = ConfigService()
    setters = {
        "provider": service.set_provider,
        "launcher": service.set_launcher,
        "model": service.set_model,
        "compatibility-policy": service.set_compatibility_policy,
    }

    setter = setters.get(key)
    if setter is None:
        expected = ", ".join(setters)
        raise typer.BadParameter(f"Unknown key '{key}'. Expected one of: {expected}")

    try:
        setter(value)
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc

    typer.echo(f"Set {key} to {value}")
