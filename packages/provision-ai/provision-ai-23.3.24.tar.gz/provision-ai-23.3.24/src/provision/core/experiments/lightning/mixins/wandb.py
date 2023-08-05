"""LightningModule mixin with custom W&B logging support."""

from typing import Any, Optional, cast

import lightning.pytorch as pl
from lightning.pytorch.loggers.logger import Logger
from lightning.pytorch.loggers.wandb import WandbLogger
from wandb.sdk.wandb_run import Run

from ....utils.metrics import LastMetric


class WandbMixin(pl.LightningModule):
    """LightningModule with easy W&B logging through self.log_wandb() and self.wandb."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the module."""
        super().__init__(*args, **kwargs)

        self.wandb: Optional[Run] = None

        self._last_epoch = LastMetric()

    @property
    def logger(self) -> Logger | None:
        """Reference to the logger object in the Trainer."""
        return self.trainer.logger if self.trainer else None

    @property
    def epoch(self) -> int:
        """Current epoch number in one-based numbering."""
        return self.current_epoch + 1 if not self.trainer.sanity_checking else self.current_epoch

    def log_wandb(self, data: dict[str, Any], step: Optional[int] = None):
        """Log data to W&B."""
        if self.wandb is not None:
            self.wandb.log(data, step=step)  # pyright: ignore[reportUnknownMemberType]

    def on_fit_start(self) -> None:
        """Pin W&B logger to self.wandb on start."""
        if isinstance(self.logger, list):
            for logger in cast(list[Logger], self.logger):
                if isinstance(logger, WandbLogger):
                    self.wandb = cast(Run, logger.experiment)  # pyright: ignore[reportUnknownMemberType]
        elif isinstance(self.logger, WandbLogger):
            self.wandb = cast(Run, self.logger.experiment)  # pyright: ignore[reportUnknownMemberType]
