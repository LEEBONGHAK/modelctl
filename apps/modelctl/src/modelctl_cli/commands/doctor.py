import typer
from rich.console import Console
from rich.table import Table

from modelctl_cli.context import container

console = Console()

_STATUS_LABELS = {
    "ok": "[green]OK[/green]",
    "warning": "[yellow]WARN[/yellow]",
    "error": "[red]ERROR[/red]",
}


def doctor() -> None:
    """Diagnose local modelctl configuration and runtime dependencies."""
    checks = container.doctor_service().run()

    table = Table(title="modelctl doctor")
    table.add_column("Check")
    table.add_column("Status")
    table.add_column("Detail")

    for check in checks:
        table.add_row(
            check.name,
            _STATUS_LABELS.get(check.status, check.status),
            check.detail,
        )

    console.print(table)

    if any(check.status == "error" for check in checks):
        raise typer.Exit(code=1)
