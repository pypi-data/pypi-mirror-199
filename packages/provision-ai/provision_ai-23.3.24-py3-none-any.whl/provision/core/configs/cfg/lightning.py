"""Lightning experiment configuration dataclasses."""

from dataclasses import dataclass
from typing import Any, Optional

from . import Settings


@dataclass
class TrainerConf:
    """Lightning Trainer configuration dataclass."""

    _target_: str = "lightning.pytorch.trainer.Trainer"
    logger: Any = True  # Union[LightningLoggerBase, Iterable[LightningLoggerBase], bool]
    enable_checkpointing: bool = True
    callbacks: Any = None  # Optional[List[Callback]]
    default_root_dir: Optional[str] = None
    gradient_clip_val: int | float | None = 0
    gradient_clip_algorithm: str | None = None
    num_nodes: int = 1
    devices: Any = None  # Union[int, str, List[int], NoneType]
    enable_progress_bar: bool = True
    overfit_batches: int | float = 0.0
    track_grad_norm: int | float | str = -1
    check_val_every_n_epoch: int | None = 1
    fast_dev_run: int | bool = False
    accumulate_grad_batches: Any = 1  # Union[int, Dict[int, int], List[list]]
    max_epochs: int | None = 1000
    min_epochs: int | None = None
    max_steps: int = -1
    min_steps: int | None = None
    max_time: Any = None  # str | timedelta | dict[str, int] | None
    limit_train_batches: int | float | None = None
    limit_val_batches: int | float | None = None
    limit_test_batches: int | float | None = None
    limit_predict_batches: int | float | None = None
    val_check_interval: int | float | None = None
    log_every_n_steps: int = 50
    accelerator: Any = None  # Union[str, Accelerator, NoneType]
    strategy: Any = None  # Union[str, Strategy, NoneType]
    sync_batchnorm: bool = False
    precision: int = 32
    enable_model_summary: bool = True
    num_sanity_val_steps: int = 2
    profiler: Any = None  # Union[BaseProfiler, bool, str, NoneType]
    benchmark: bool = False
    deterministic: bool = False
    reload_dataloaders_every_n_epochs: int = 0
    replace_sampler_ddp: bool = True
    detect_anomaly: bool = False
    plugins: Any = None  # Union[str, list, NoneType]
    multiple_trainloader_mode: str = "max_size_cycle"
    inference_mode: bool = True


@dataclass
class LightningConf(TrainerConf):
    """Lightning Trainer configuration with Provision AI default overrides."""

    deterministic: bool = True
    accelerator: str = "gpu"
    devices: int = 1


@dataclass
class LightningSettings(Settings):
    """Default Lightning experiment settings."""

    # Lightning trainer settings
    pl: LightningConf = LightningConf()

    # Additional experiment settings
    validate_before_training: bool = True
    save_checkpoints: bool = True

    resume_path: Optional[str] = None
