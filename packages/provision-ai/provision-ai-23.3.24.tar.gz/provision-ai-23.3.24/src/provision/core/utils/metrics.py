"""Base experiment metrics."""

from dataclasses import dataclass
from typing import cast

import torch
import torch.nn as nn
import torchmetrics
import torchmetrics.classification.accuracy
from torch import Tensor

from .enums import Phase


class Metrics(nn.Module):
    """Metrics container."""

    class Collection(nn.Module):
        """Epoch-level metrics."""

        @dataclass
        class Settings:
            """Metrics settings."""

            num_classes: int

        def __init__(self, settings: Settings) -> None:
            """Initialize default metrics."""
            super().__init__()

            self.loss = torchmetrics.MeanMetric()
            self.accuracy = cast(
                torchmetrics.classification.accuracy.MulticlassAccuracy,
                torchmetrics.Accuracy(task="multiclass", num_classes=settings.num_classes),
            )

        def __iter__(self):
            """Iterate over metrics."""
            return (
                (name, module) for name, module in self._modules.items() if isinstance(module, torchmetrics.Metric)
            )

    def __init__(self, settings: Collection.Settings) -> None:
        """Initialize training/validation metrics collections."""
        super().__init__()

        self._metrics = {
            Phase.TRAINING: self.Collection(settings),
            Phase.VALIDATION: self.Collection(settings),
        }

        self.add_module(Phase.TRAINING.name, self._metrics[Phase.TRAINING])
        self.add_module(Phase.VALIDATION.name, self._metrics[Phase.VALIDATION])

    def __getitem__(self, key: Phase | str) -> Collection:
        """Return metrics collection for the given phase."""
        if isinstance(key, str):
            return self._metrics[Phase[key]]
        else:
            return self._metrics[key]


class LastMetric(torchmetrics.Metric):
    """Metric for storing the latest value."""

    def __init__(self) -> None:
        """Initialize placeholder for last value of the metric."""
        super().__init__()

        self.last: Tensor

        self.add_state(  # pyright: ignore[reportUnknownMemberType]
            "last", default=torch.tensor(0), dist_reduce_fx="max"
        )

    def update(self, value: Tensor | int | float) -> None:  # pyright: ignore[reportIncompatibleMethodOverride]
        """Update the metric with the latest value."""
        self.last = torch.tensor(value)

    def compute(self) -> Tensor:  # pyright: ignore[reportIncompatibleMethodOverride]
        """Return the last value of the metric."""
        return self.last
