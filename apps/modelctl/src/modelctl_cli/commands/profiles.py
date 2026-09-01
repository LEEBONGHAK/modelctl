import typer
from rich.console import Console
from rich.table import Table

from modelctl_cli.context import container
from modelctl_core.services.profile_service import Profile

profiles_app = typer.Typer(help="Save and apply named modelctl configurations.")
console = Console()


def _profile_service():
    return container.profile_service()


def _bad_parameter(error: ValueError) -> typer.BadParameter:
    return typer.BadParameter(str(error))


def _add_profile_row(table: Table, profile: Profile) -> None:
    table.add_row(
        profile.name,
        profile.provider,
        profile.model,
        profile.launcher,
        profile.compatibility_policy,
    )


@profiles_app.command("save")
def save_profile(name: str) -> None:
    """Save the current provider, model, launcher, and compatibility policy."""
    try:
        profile = _profile_service().save(name)
    except ValueError as error:
        raise _bad_parameter(error) from error
    console.print(f"[green]Saved profile:[/green] {profile.name}")


@profiles_app.command("list")
def list_profiles() -> None:
    """List named profiles."""
    try:
        profiles = _profile_service().list()
    except ValueError as error:
        raise _bad_parameter(error) from error

    if not profiles:
        console.print("[yellow]No saved profiles.[/yellow]")
        return

    table = Table(title="Named profiles")
    table.add_column("Name")
    table.add_column("Provider")
    table.add_column("Model")
    table.add_column("Launcher")
    table.add_column("Policy")
    for profile in profiles:
        _add_profile_row(table, profile)
    console.print(table)


@profiles_app.command("show")
def show_profile(name: str) -> None:
    """Show one named profile."""
    try:
        profile = _profile_service().get(name)
    except ValueError as error:
        raise _bad_parameter(error) from error

    table = Table(title=f"Profile: {profile.name}")
    table.add_column("Name")
    table.add_column("Provider")
    table.add_column("Model")
    table.add_column("Launcher")
    table.add_column("Policy")
    _add_profile_row(table, profile)
    console.print(table)


@profiles_app.command("use")
def use_profile(name: str) -> None:
    """Validate and atomically apply one named profile."""
    try:
        profile = _profile_service().use(name)
    except ValueError as error:
        raise _bad_parameter(error) from error
    console.print(f"[green]Applied profile:[/green] {profile.name}")


@profiles_app.command("delete")
def delete_profile(name: str) -> None:
    """Delete one named profile."""
    try:
        profile = _profile_service().delete(name)
    except ValueError as error:
        raise _bad_parameter(error) from error
    console.print(f"[green]Deleted profile:[/green] {profile.name}")
