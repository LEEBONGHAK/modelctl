import typer
from rich.prompt import Prompt

from modelctl_core.services.auth_service import AuthService

auth_app = typer.Typer()

@auth_app.command()
def login(provider: str):
    token = Prompt.ask(
        "API Key",
        password=True,
    )

    AuthService().save(
        provider,
        token,
    )

    print("Saved.")