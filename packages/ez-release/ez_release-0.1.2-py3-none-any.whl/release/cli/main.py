from typing import Optional

from rich.console import Console
from rich.table import Table
from typer import Typer
import typer

from release.cli.bump import Parts, raise_on_non_main_branch, raise_on_dirty
from release.cli.helpers import exit_nicely, get_current_repo
from release.constants import PACKAGE_NAME
from release.core import (
    get_latest_release,
    get_next_release,
    get_sorted_releases_by_domains,
)
from release.exceptions import ReleaseException

app = Typer(add_completion=False)

console = Console()


def show_version(flag: bool):
    if flag:
        from importlib.metadata import version

        console.print(f"release [bold]{version(PACKAGE_NAME)}[bold]")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        None, "--version", callback=show_version, help="Show version."
    ),
):
    """Make release"""


@app.command()
@exit_nicely
def bump(
    part: Parts = typer.Option(
        "patch", "--part", "-p", help="Part of version to bump."
    ),
    domain: Optional[str] = typer.Option(
        None, "--domain", "-d", help="Which domain to bump (if applicable)"
    ),
    push: bool = typer.Option(False, help="Whether to push tag to remote origin"),
    dry_run: bool = False,
    allow_non_main: bool = typer.Option(
        False, help="Whether to allow tagging a non main branch"
    ),
):
    """
    Bump version.
    """
    repo = get_current_repo()

    if not allow_non_main:
        raise_on_non_main_branch(repo)

    raise_on_dirty(repo)
    console.print("Pulling ...")
    repo.remotes.origin.pull(rebase=True)

    current_release = get_latest_release(repo, domain=domain, domain_separator=None)
    next_release = get_next_release(current_release, part=part.value)

    if dry_run:
        console.print("Dry run. None of the following will actually run.")
        console.print(f"Bumping {current_release} --> {next_release}")
    else:
        typer.echo(f"Bumping {current_release} --> {next_release}")
        repo.create_tag(f"{next_release}")
        if push:
            console.print(f"Pushing tag {next_release} to remote ...")
            repo.remotes.origin.push(f"{next_release}")


@app.command()
@exit_nicely
def list(
    domain: Optional[str] = typer.Option(
        None, "--domain", "-d", help="Domain to consider (if applicable)"
    ),
    all_domains: bool = False,
    latest: bool = False,
):
    """List releases."""
    repo = get_current_repo()
    console.print("Pulling ...")
    repo.remotes.origin.pull(rebase=True)

    releases = get_sorted_releases_by_domains(repo, domain_separator=None)

    if not all_domains:
        if domain not in releases:
            raise ReleaseException(f"Domain '{domain}' does not exists")
        releases = {domain: releases[domain]}

    if latest:
        releases = {domain: rel[-1:] for domain, rel in releases.items()}

    table = Table(show_header=True)
    table.add_column("domain")
    table.add_column("version", style="bold")
    for domain, rels in releases.items():
        for rel in rels:
            table.add_row(domain or "-", f"{rel}".split(rel.domain_separator)[-1])
    console.print(table)
