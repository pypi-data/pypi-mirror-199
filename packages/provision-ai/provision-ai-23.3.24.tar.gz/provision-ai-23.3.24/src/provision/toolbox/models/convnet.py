"""Basic convolutional neural network."""

import torch
import torch.nn as nn


class ConvNet(nn.Module):
    """
    Basic convolutional neural network.

    Architecture adapted from https://www.kaggle.com/adityav5/cnn-on-fashion-mnist-approx-95-test-accuracy.
    """

    def __init__(
        self,
        in_channels: int,
        input_shape: tuple[int, int],
        num_classes: int,
    ):
        """Create a convnet module.

        Parameters
        ----------
        in_channels : int
            Number of data channels.
        input_shape : tuple[int, int]
            Input dimensions (H, W).
        num_classes : int
            Number of output classes.

        """
        super().__init__()

        self.in_channels = in_channels
        self.height = input_shape[0]
        self.width = input_shape[1]
        self.n_classes = num_classes

        self.conv = nn.Sequential(
            nn.Conv2d(in_channels=self.in_channels, out_channels=64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(num_features=64),
            nn.MaxPool2d(kernel_size=2),
            nn.Dropout2d(p=0.3),
            nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(in_channels=128, out_channels=128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(num_features=128),
            nn.MaxPool2d(kernel_size=2),
            nn.Dropout(p=0.3),
            nn.Conv2d(in_channels=128, out_channels=256, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(in_channels=256, out_channels=256, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.BatchNorm2d(num_features=256),
            nn.MaxPool2d(kernel_size=2),
            nn.Dropout(p=0.3),
        )

        self.flatten = nn.Flatten(start_dim=1)

        self.dense = nn.Sequential(
            nn.Linear(in_features=256 * (self.height // 8) * (self.width // 8), out_features=2048),
            nn.ReLU(),
            nn.Dropout(p=0.3),
            nn.Linear(in_features=2048, out_features=512),
            nn.ReLU(),
            nn.Linear(in_features=512, out_features=self.n_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:  # pyright: ignore[reportIncompatibleMethodOverride]
        """Forward pass a batch of examples (N, C, H, W) -> (N, n_classes)."""
        x = self.conv(x)
        x = self.flatten(x)
        x = self.dense(x)

        return x
