"""Main experiment system."""

from abc import ABC, abstractmethod
from typing import Any

import lightning.pytorch as pl
import torch.nn as nn
from torch import Tensor

from ...core.configs.cfg import Settings
from ...core.experiments import NoTrainMixin, WandbMixin
from ...core.utils.enums import Phase
from ...core.utils.metrics import Metrics

# TODO: Generic typing


class BaseSystem(
    NoTrainMixin,
    WandbMixin,
    pl.LightningModule,
    ABC,
):
    """Basic model with loss system."""

    def __init__(
        self,
        cfg: Settings,
    ):
        """Define basic system attributes and save Lightning hyperparameters."""
        super().__init__()
        self.save_hyperparameters()

        self.cfg = cfg
        """Main experiment config."""

        # Model
        self.model: nn.Module
        """Main model instance."""

        self.criterion: nn.Module
        """Loss function."""

        # Metrics
        self.metrics: Metrics
        """System metrics collection."""

    def _verify_init(self):
        # TODO: Verify
        fields = ["cfg", "model", "criterion", "metrics"]

        for field in fields:
            assert getattr(self, field) is not None

    # Forward
    # ----------------------------------------------------------------------------------------------
    def forward(self, x: Tensor) -> Tensor:  # pyright: ignore[reportIncompatibleMethodOverride]
        """Perform default forward pass."""
        return self.model(x)

    def calculate_loss(self, outputs: Tensor, targets: Tensor) -> Tensor:
        """Return loss value for the given batch."""
        return self.criterion(outputs, targets)

    @abstractmethod
    def step(self, batch: list[Tensor], batch_idx: int, *, phase: Phase) -> Tensor:
        """Forward and compute loss on given batch (training/validation)."""
        pass

    def log_step(
        self,
        phase: Phase,
    ) -> None:
        """Log metrics."""
        for name, metric in self.metrics[phase]:
            if name.startswith("loss"):
                self.log(  # pyright: ignore[reportUnknownMemberType]
                    f"{phase.name.lower()}/{name.replace('_', '/')}", metric
                )
            else:
                self.log(f"{phase.name.lower()}/metric/{name}", metric)  # pyright: ignore[reportUnknownMemberType]

        self._last_epoch(self.epoch)
        self.log("epoch", self._last_epoch)  # pyright: ignore[reportUnknownMemberType]

    # Training
    # ----------------------------------------------------------------------------------------------
    def training_step(  # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        batch: list[Tensor],
        batch_idx: int,
    ) -> Tensor:
        """Perform a single training step."""
        loss = self.step(batch, batch_idx, phase=Phase.TRAINING)
        self.log_step(phase=Phase.TRAINING)
        return loss

    # Validation
    # ----------------------------------------------------------------------------------------------
    def validation_step(  # pyright: ignore[reportIncompatibleMethodOverride]
        self,
        batch: list[Tensor],
        batch_idx: int,
    ) -> Tensor:
        """Perform a single validation step."""
        loss = self.step(batch, batch_idx, phase=Phase.VALIDATION)
        self.log_step(phase=Phase.VALIDATION)
        return loss

    # Optimizers
    # ----------------------------------------------------------------------------------------------
    @abstractmethod
    def configure_optimizers(self) -> Any:
        """Attach optimizer to the model."""
        pass
