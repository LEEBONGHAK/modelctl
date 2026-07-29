import shutil
import sys

from rich.table import Table

from modelctl.core.paths import (
    config_file,
    database_file,
)

from modelctl.services.credential import (
    get_secret,
)



def run_doctor(console):


    table = Table(
        title="modelctl doctor"
    )


    table.add_column(
        "Component"
    )

    table.add_column(
        "Status"
    )


    table.add_row(
        "Python",
        sys.version.split()[0]
    )


    table.add_row(
        "Claude Code",
        "OK"
        if shutil.which("claude")
        else "Missing"
    )


    table.add_row(
        "Git",
        "OK"
        if shutil.which("git")
        else "Missing"
    )


    table.add_row(
        "Config",
        "OK"
        if config_file().exists()
        else "Missing"
    )


    table.add_row(
        "Database",
        "OK"
        if database_file().exists()
        else "Missing"
    )


    table.add_row(
        "OpenRouter Key",
        "OK"
        if get_secret("openrouter")
        else "Not configured"
    )


    console.print(table)
