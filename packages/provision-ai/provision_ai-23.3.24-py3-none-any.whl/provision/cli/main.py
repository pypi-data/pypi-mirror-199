"""CLI for experiment provisioning."""

# pyright: reportUnknownMemberType=false

import shutil
from contextlib import suppress
from pathlib import Path
from typing import Any, cast

import typer
from copier import run_auto  # type: ignore
from git import GitCommandError
from git.repo import Repo
from rich import print
from rich.panel import Panel
from rich.prompt import Confirm

RENDER_BRANCH = "render"
BASE_BRANCH = "base"

app = typer.Typer()
template = typer.Typer()

app.add_typer(template, name="template")


class CLI:
    """CLI state container."""

    template_dir: Path
    template_repo: Repo
    render_dir: Path
    render_repo: Repo


@app.callback()
def callback() -> None:
    """AI experiment provisioner."""
    pass


@app.command()
def create():
    """Create new project based on a given template."""
    raise NotImplementedError


@template.callback()
def template_callback():
    """Manage experiment templates."""
    pass


def _setup_repos(template_dir: Path) -> None:
    try:
        CLI.template_dir = template_dir.resolve(strict=True)
    except FileNotFoundError:
        print(f"[bold red]Template directory [white]{template_dir}[/white] does not exist[/]")
        raise typer.Abort
    try:
        CLI.template_repo = Repo(CLI.template_dir)
        assert not CLI.template_repo.bare, "Template directory is not a git repository"
    except Exception:
        print(f"[bold red]Template directory [white]{CLI.template_dir}[/white] is not a valid git repository[/]")
        raise typer.Abort

    CLI.render_dir = (CLI.template_dir / "..").resolve(strict=True)
    CLI.render_dir = CLI.render_dir / f"{CLI.template_dir.name}.rendered"


@template.command("edit")
def template_edit(template_dir: Path):
    """Render template for editing."""
    _setup_repos(template_dir)

    if CLI.render_dir.exists():
        if not Confirm.ask(f"Rendered directory [bold white]{CLI.render_dir}[/bold white] already exists. Overwrite?"):
            return

        shutil.rmtree(CLI.render_dir)

    print(
        Panel.fit(
            f"[bold yellow]Rendering:\n"
            f"(source) :right_arrow: [white] {CLI.template_dir}[/white]\n"
            f"(target) :right_arrow: [white] {CLI.render_dir}[/white][/]"
        )
    )
    CLI.template_repo.git.worktree("prune")
    CLI.template_repo.git.worktree("add", CLI.render_dir, "-B", RENDER_BRANCH)

    CLI.render_repo = Repo(CLI.render_dir)
    assert not CLI.render_repo.bare, "Could not create a git repository for the rendered template"

    CLI.render_repo.git.rm("-rf", ".")
    CLI.render_repo.git.clean("-fdx")

    run_auto(
        str(CLI.template_dir),
        str(CLI.render_dir),
        data={"project": "Experiment", "customize": False},
        vcs_ref="HEAD",
    )

    CLI.render_repo.git.add("-A")
    CLI.render_repo.git.commit("-m", "Template render")

    CLI.render_repo.git.branch("-f", BASE_BRANCH)


@template.command("save")
def template_save(template_dir: Path):
    """Update template with changes from the render directory."""
    _setup_repos(template_dir)

    CLI.render_repo = Repo(CLI.render_dir)
    assert not CLI.render_repo.bare, f"{CLI.render_dir} is not a valid git repository"

    with suppress(GitCommandError):
        CLI.render_repo.git.add("-A")
        CLI.render_repo.git.commit("-m", "Save changes")

    head: str = getattr(CLI.render_repo.heads, RENDER_BRANCH).commit.hexsha
    base: str = getattr(CLI.render_repo.heads, BASE_BRANCH).commit.hexsha

    try:
        CLI.template_repo.git.cherry_pick("--quit")
        CLI.template_repo.git.cherry_pick("-n", f"{base}..{head}")
    except GitCommandError as e:
        print("[bold red]Cherry pick failed...[/]")
        print(cast(Any, e).stderr)
        raise typer.Abort


@template.command("clean")
def template_clean(template_dir: Path):
    """Clean rendered template worktree."""
    _setup_repos(template_dir)

    print(Panel.fit(f"[bold yellow]Cleaning up:\n" f"(target) :right_arrow: [white] {CLI.render_dir}[/white][/]"))

    if CLI.render_dir.exists():
        if not Confirm.ask(f"Do you want to remove the [bold white]{CLI.render_dir}[/bold white] directory?"):
            return

        shutil.rmtree(CLI.render_dir)

    CLI.template_repo.git.worktree("prune")
    with suppress(GitCommandError):
        CLI.template_repo.git.branch("-D", BASE_BRANCH)

    with suppress(GitCommandError):
        CLI.template_repo.git.branch("-D", RENDER_BRANCH)
