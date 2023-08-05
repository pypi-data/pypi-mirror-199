"""Base experiment class."""

import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Type

import hydra
import lovely_tensors as lt  # type: ignore
import setproctitle
from dotenv import load_dotenv
from dotenv.main import find_dotenv
from omegaconf import OmegaConf
from rich import print
from rich.console import Group
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text

from .configs import RootConfig, Settings, register_configs
from .utils.logging import info_bold
from .utils.random import seed_everything
from .utils.rundir import create_rundir, finalize_rundir, save_state

load_dotenv(find_dotenv(usecwd=True))
lt.monkey_patch()  # type: ignore[reportUnknownMemberType]


class Experiment(ABC):
    """Deep learning experiment handler."""

    def __init__(self, settings_cls: Type[Settings], *, settings_group: Optional[str] = None) -> None:
        """Run an experiment from a provided entry point with minimal boilerplate code.

        Incorporates run directory setup and Hydra support.
        """
        self.settings_cls = settings_cls
        self.settings_group = settings_group
        self.root_cfg: RootConfig

        self._set_env()
        self._prepare_rundir()

        # TODO
        # Hydra will change workdir to the run dir before calling `self.main`
        register_configs(self.settings_cls, self.settings_group)
        hydra_decorator = hydra.main(config_path=".", config_name="root", version_base="1.1")
        hydra_decorator(self.entry)()

        self.finish()

    def _set_env(self) -> None:
        assert os.getenv("DATA_DIR") is not None, "Missing DATA_DIR environment variable."
        assert os.getenv("RESULTS_DIR") is not None, "Missing RESULTS_DIR environment variable."
        assert os.getenv("WANDB_PROJECT") is not None, "Missing WANDB_PROJECT environment variable."
        assert os.getenv("WANDB_ENTITY") is not None, "Missing WANDB_ENTITY environment variable."
        os.environ["DATA_DIR"] = str(Path(os.environ["DATA_DIR"]).expanduser())
        os.environ["RESULTS_DIR"] = str(Path(os.environ["RESULTS_DIR"]).expanduser())

    def _prepare_rundir(self):
        create_rundir()
        save_state()
        self.on_before_chdir()

    def entry(self, root_cfg: RootConfig) -> None:
        """Experiment entrypoint. Called after initial setup with `root_cfg` populated by Hydra."""
        info_bold("Executing main experiment entrypoint.")

        self.root_cfg = root_cfg
        self.cfg = root_cfg.cfg

        RUN_NAME = os.getenv("RUN_NAME")
        cfg = OmegaConf.to_yaml(self.root_cfg, resolve=True)

        print(
            Panel(
                Group(
                    Text.from_markup(f"[bold yellow]Run name :arrow_forward: [white]{RUN_NAME}[/]\n"),
                    Text.from_markup("[bold yellow]Loaded configuration values:[/]"),
                    Syntax(cfg, "yaml", theme="dracula", word_wrap=True, padding=1, dedent=True),
                ),
                title=f"Experiment {RUN_NAME}",
                border_style="bold yellow",
            )
        )

        Path(f"{os.environ['RUN_DIR']}/code.cfg").write_text(cfg + "\n")

        setproctitle.setproctitle(f'{RUN_NAME} ({os.getenv("WANDB_PROJECT")})')

        seed_everything(root_cfg.cfg.seed)
        self.main()

    @abstractmethod
    def main(self) -> None:
        """Run main experiment logic."""
        pass

    def finish(self) -> None:
        """Finish experiment. Called after `main` returns."""
        self.on_before_finish()
        finalize_rundir()

    def on_before_chdir(self) -> None:
        """Provide a hook before Hydra changes working directory to the run directory."""
        pass

    def on_before_finish(self) -> None:
        """Provide a hook before run directory is finalized."""
        pass
