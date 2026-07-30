import typer

from modelctl_core.services.config_service import ConfigService

config_app = typer.Typer()


@config_app.command("show")
def show():
    cfg = ConfigService().get()
    print(cfg.model_dump())


@config_app.command("set")
def set_value(
    key: str,
    value: str,
):
    service = ConfigService()

    if key == "provider":
        service.set_provider(value)

    elif key == "launcher":
        service.set_launcher(value)

    else:
        raise typer.BadParameter(key)
