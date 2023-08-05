"""Lightning-based experiment."""

import os
import textwrap
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Optional, Type, TypeVar, cast

import hydra
import lightning.pytorch as pl
from lightning.pytorch.callbacks import ModelCheckpoint
from lightning.pytorch.callbacks.progress.rich_progress import (
    RichProgressBar,
    RichProgressBarTheme,
)
from lightning.pytorch.loggers.wandb import WandbLogger
from lightning.pytorch.trainer.states import TrainerState
from omegaconf import OmegaConf
from omegaconf.dictconfig import DictConfig
from rich import print
from rich.console import Group
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text
from wandb.sdk.wandb_run import Run

from ...configs import get_tags
from ...configs.cfg.lightning import LightningSettings
from ...main import Experiment
from ...utils.callbacks import CustomRichModelSummary
from ...utils.logging import error

T = TypeVar("T", bound="LightningExperiment")


class LightningExperiment(Experiment):
    """A deep learning experiment based on Lightning with Hydra and W&B support."""

    def __new__(cls: Type[T], *args: Any, **kwargs: Any) -> T:
        """Create a new instance of the experiment with the actual `main` wrapped with pre-/post-init functionality."""
        setattr(cls, "main", cls.main_wrap(cls.main))

        return super().__new__(cls)

    def on_before_chdir(self) -> None:
        """Proceed with experiment-specific init, setup the W&B logger and pin it to self.run."""
        super().on_before_chdir()

        self.cfg: LightningSettings

        self.wandb_logger: WandbLogger
        self.datamodule: Optional[pl.LightningDataModule] = None
        self.system: Optional[pl.LightningModule] = None
        self.callbacks: list[Any] = []
        self.trainer: Optional[pl.Trainer] = None

        assert os.getenv("WANDB_PROJECT") is not None, "Missing WANDB_PROJECT environment variable."

        self.wandb_logger = WandbLogger(
            project=cast(str, os.getenv("WANDB_PROJECT")),
            entity=os.getenv("WANDB_ENTITY"),
            name=os.getenv("RUN_NAME"),
            save_dir=str(Path(os.getenv("RUN_DIR", "."))),
        )

        # Init logger from source dir (code base) before switching to run dir (results)
        cast(Any, self.wandb_logger).experiment  # Bare access for initialization
        self.run: Run = cast(Any, self.wandb_logger).experiment

    @classmethod
    def main_wrap(cls, main: Callable[[T], None]) -> Callable[[T], None]:
        """Wrap the actual `main` function with pre-/post-init functionality."""

        @wraps(main)
        def wrapped(self: T):
            # Pre-main
            tags = get_tags(cast(DictConfig, self.root_cfg))
            self.run.tags = tags
            self.run.notes = str(self.root_cfg.notes)
            self.wandb_logger.log_hyperparams(OmegaConf.to_container(self.root_cfg.cfg, resolve=True))  # type: ignore

            Path(self.root_cfg.data_dir).mkdir(parents=True, exist_ok=True)
            self.setup_datamodule()

            self.setup_system()

            # Experiment main
            main(self)

            # Check if training was already handled by main()
            if self.trainer and cast(TrainerState, self.trainer.state).finished:  # pyright: ignore
                return

            # Post-main setup, automatic training
            if not self.callbacks:
                self.setup_callbacks()

            if not self.trainer:
                self.setup_trainer()

            assert self.trainer is not None
            assert (
                self.system is not None
            ), "A main LightningModule should be assigned to self.system inside setup_system() or main()."

            print(
                Panel(
                    Group(
                        Syntax(str(self.system), "maql", theme="dracula", word_wrap=True, padding=1, dedent=True),
                    ),
                    title="System architecture",
                    border_style="bold yellow",
                )
            )

            self.fit()

        return wrapped

    def main(self, /) -> None:
        """Define the main experiment logic.

        Should be overridden by subclasses.
        """
        pass

    def setup_datamodule(self) -> None:
        """Define the main datamodule.

        Should be overridden by subclasses.
        """
        pass

    def setup_system(self) -> None:
        """Define the main system.

        Should be overridden by subclasses.
        """
        pass

    def setup_callbacks(self) -> None:
        """Attach checkpointing and progress bar callbacks."""
        if self.cfg.save_checkpoints:
            checkpointer = ModelCheckpoint(
                dirpath="checkpoints",
                filename="epoch{epoch:02d}",
                auto_insert_metric_name=False,
                every_n_epochs=1,
                save_on_train_epoch_end=True,
                save_weights_only=False,
            )

            self.callbacks.append(checkpointer)

        progress_bar = RichProgressBar(
            theme=RichProgressBarTheme(
                description="green_yellow",
                progress_bar="green1",
                progress_bar_finished="green1",
                progress_bar_pulse="#6206E0",
                batch_progress="green_yellow",
                time="grey82",
                processing_speed="grey82",
                metrics="grey82",
            ),
            refresh_rate=1,
        )

        self.callbacks.append(progress_bar)
        summary = CustomRichModelSummary(max_depth=-1)

        self.callbacks.append(summary)

    def setup_trainer(self) -> None:
        """Create a standard Lightning trainer."""
        num_sanity_val_steps = -1 if self.cfg.validate_before_training else 0

        # TODO: Add resume support

        if num_sanity_val_steps != self.cfg.pl.num_sanity_val_steps:
            overrides = textwrap.dedent(
                f"""
                cfg:
                  pl:
                    num_sanity_val_steps: {num_sanity_val_steps}
                """
            ).strip()

            print(
                Panel(
                    Group(
                        Text.from_markup(
                            "[bold yellow]Overriding config settings with dynamically derived values:[/]"
                        ),
                        Syntax(overrides, "yaml", theme="dracula", word_wrap=True, padding=1, dedent=True),
                    ),
                    title="Config overrides",
                    border_style="bold yellow",
                )
            )

        self.trainer = hydra.utils.instantiate(
            self.cfg.pl,
            logger=self.wandb_logger,
            callbacks=self.callbacks,
            enable_checkpointing=self.cfg.save_checkpoints,
            num_sanity_val_steps=num_sanity_val_steps,
            enable_model_summary=False,
        )

    def fit(self) -> None:
        """Start training using the defined system/datamodule combination."""
        assert self.system
        assert self.trainer
        self.trainer.fit(  # pyright: ignore[reportUnknownMemberType]
            self.system,
            datamodule=self.datamodule,
            ckpt_path=self.cfg.resume_path,
        )

    def on_before_finish(self) -> None:
        """Raise error code if training was interrupted."""
        assert self.trainer
        if self.trainer.interrupted:
            error("Training interrupted.")
            self.run.finish(exit_code=255)  # pyright: ignore[reportUnknownMemberType]
        else:
            self.run.finish()  # pyright: ignore[reportUnknownMemberType]
