from typing import Annotated

import typer
from rich.console import Console
from rich.prompt import Prompt

from modelctl_core.auth.service import CredentialStorageError

from modelctl_cli.context import container

auth_app = typer.Typer(help="Manage provider credentials.")
console = Console()


@auth_app.command()
def login(
    provider: str,
    allow_plaintext_fallback: Annotated[
        bool,
        typer.Option(
            "--allow-plaintext-fallback",
            help=(
                "Allow user-private file storage only when the operating-system "
                "keyring is unavailable."
            ),
        ),
    ] = False,
) -> None:
    """Store a provider API credential without displaying it."""
    token = Prompt.ask("API Key", password=True)

    try:
        storage = container.credentials.save(
            provider,
            token,
            allow_plaintext_file=allow_plaintext_fallback,
        )
    except ValueError as error:
        raise typer.BadParameter(str(error)) from error
    except CredentialStorageError as error:
        console.print(f"[red]{error}[/red]")
        raise typer.Exit(code=1) from error

    if storage == "file":
        console.print(
            "[yellow]Credential saved to a user-private plaintext file because "
            "the keyring was unavailable.[/yellow]"
        )
    else:
        console.print("[green]Credential saved to the operating-system keyring.[/green]")
