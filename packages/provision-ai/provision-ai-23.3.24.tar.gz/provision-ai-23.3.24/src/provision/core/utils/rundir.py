"""Experiment working directory management."""

import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, cast

import coolname  # type: ignore
from dotenv import load_dotenv
from git.repo import Repo
from rich import print

load_dotenv()


def create_rundir():
    """Create a separate working directory under `$RESULTS_DIR/$WANDB_PROJECT` with a randomly generated run name."""
    date = datetime.now().strftime("%Y%m%d-%H%M")
    name: str = cast(Any, coolname).generate_slug(2)
    os.environ["RUN_NAME"] = f"{date}-{name}"

    results_root = f'{os.getenv("RESULTS_DIR")}/{os.getenv("WANDB_PROJECT")}'
    if os.getenv("RUN_MODE", "").lower() == "debug":
        run_dir = f'{results_root}/debug/{os.getenv("RUN_NAME")}'
        completed_run_dir = run_dir
        os.environ["WANDB_MODE"] = "disabled"
    else:
        run_dir = f'{results_root}/running/{os.getenv("RUN_NAME")}'
        completed_run_dir = f'{results_root}/completed/{os.getenv("RUN_NAME")}'

    os.makedirs(run_dir, exist_ok=True)
    os.environ["RUN_DIR"] = run_dir
    os.environ["COMPLETED_RUN_DIR"] = completed_run_dir


def finalize_rundir():
    """Move the run directory to completed subdirectory."""
    run_dir = Path(os.getenv("RUN_DIR", ""))
    completed_run_dir = Path(os.getenv("COMPLETED_RUN_DIR", ""))

    if run_dir != completed_run_dir:
        assert run_dir.exists() and run_dir.is_dir()
        assert not completed_run_dir.exists()
        os.makedirs(completed_run_dir.parent, exist_ok=True)
        run_dir.rename(completed_run_dir)


def save_state() -> None:
    """Save the current git state and pending changes to the run directory."""
    try:
        src_repo = Repo(".")
        dst_repo = Repo.clone_from(  # pyright: ignore[reportUnknownMemberType]
            url=".", to_path=str(Path(f"{os.environ['RUN_DIR']}/code"))
        )
        cast(Any, dst_repo).git.checkout("-b", os.getenv("RUN_NAME"))

        # Git state
        git_status = f"{str(cast(Any, src_repo).head.commit.hexsha)}\n{str(cast(Any, src_repo).head.commit.message)}"
        Path(f"{os.environ['RUN_DIR']}/code.git").write_text(git_status, encoding="utf-8")

        # Pending changes
        pending_diff: str = src_repo.git.diff("HEAD~0")  # pyright: ignore[reportUnknownMemberType]

        if pending_diff:
            Path(f"{os.environ['RUN_DIR']}/code.diff").write_text(pending_diff + "\n", encoding="utf-8")

            dst_repo.git.apply(  # pyright: ignore[reportUnknownMemberType]
                ["-3", f"{os.environ['RUN_DIR']}/code.diff"]
            )
            dst_repo.index.commit("Save uncommitted code changes")  # pyright: ignore[reportUnknownMemberType]
    except Exception:
        print(":exclamation:[bold yellow]Code state saving failed. Maybe not running from a git repository?")

    # Cmd line
    Path(f"{os.environ['RUN_DIR']}/code.cmd").write_text(" ".join(sys.argv) + "\n")
