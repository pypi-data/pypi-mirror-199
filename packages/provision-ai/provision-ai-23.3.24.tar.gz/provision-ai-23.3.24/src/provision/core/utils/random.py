"""PRNG seeders."""

import random

import numpy.random
import torch


def seed_everything(seed: int) -> None:
    """Seed all PRNGs with a given seed."""
    random.seed(seed)
    numpy.random.seed(seed)
    torch.manual_seed(seed)  # pyright: ignore[reportUnknownMemberType]
    torch.cuda.manual_seed_all(seed)
