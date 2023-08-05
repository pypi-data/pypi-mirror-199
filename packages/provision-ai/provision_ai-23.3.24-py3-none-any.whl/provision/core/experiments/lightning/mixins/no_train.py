"""LightningModule mixin with disabled training context."""

from contextlib import contextmanager

import lightning.pytorch as pl
import torch


class NoTrainMixin(pl.LightningModule):
    """Mixin to enable self.no_train() context manager."""

    @contextmanager
    def no_train(self):
        """Context manager to temporarily disable training mode and gradient computations."""
        training = self.training
        self.train(False)
        with torch.no_grad():
            yield
        self.train(training)
