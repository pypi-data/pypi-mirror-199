import os
from functools import wraps

import typer
from git import Repo
from rich.console import Console

from release.exceptions import ReleaseException


console = Console()


def exit_nicely(f):
    """Catches expected exception and exit CLI nicely."""

    @wraps(f)
    def _wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ReleaseException as err:
            console.print(f"[red]{err.msg}[red]")
            raise typer.Exit(1)

    return _wrapper


def get_current_repo() -> Repo:
    return Repo(os.getcwd(), search_parent_directories=True)
