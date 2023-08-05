"""Root level imports for `provision.core`."""

import warnings

from .configs import RootConfig as RootConfig
from .configs import Settings as Settings
from .main import Experiment as Experiment
from .utils.enums import Phase as Phase
from .utils.logging import debug as debug
from .utils.logging import error as error
from .utils.logging import info as info
from .utils.logging import info_bold as info_bold
from .utils.logging import warning as warning
from .utils.metrics import Metrics as Metrics

# pytorch_lightning -> lightning.pytorch depreciation support
# TODO: Remove this once the support for pytorch_lightning is no longer needed

# isort: split

import sys

import lightning
import lightning.pytorch
import lightning.pytorch.loggers

sys.modules["pytorch_lightning"] = lightning.pytorch
sys.modules["pytorch_lightning.loggers"] = lightning.pytorch.loggers

import pytorch_lightning.loggers  # noqa: E402


def _pl_loggers__getattr__(name: str):
    warnings.warn(
        "pytorch_lightning.loggers.LightningLoggerBase has been deprecated in favor of Logger, "
        "using temporary name mangling.",
        FutureWarning,
    )
    if name == "LightningLoggerBase":
        name = "Logger"
    return getattr(globals()["pytorch_lightning"].loggers, name)


setattr(pytorch_lightning.loggers, "__getattr__", _pl_loggers__getattr__)
