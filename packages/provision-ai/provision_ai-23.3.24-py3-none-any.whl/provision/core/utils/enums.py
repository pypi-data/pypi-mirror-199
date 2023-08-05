"""Helper enums."""
from enum import Enum, auto


class Phase(Enum):
    """Dataset used for training."""

    TRAINING = auto()
    VALIDATION = auto()
