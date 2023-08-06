from typing import Optional

import wandb
import subprocess

from pytorch_lightning import Callback, Trainer, LightningModule
from pytorch_lightning.loggers import LoggerCollection, WandbLogger
from pathlib import Path
from pytorch_lightning.utilities import rank_zero_only
from hydra.core.hydra_config import HydraConfig


def get_wandb_logger(trainer: Trainer) -> WandbLogger:
    """Safely get Weights&Biases logger from Trainer."""

    if trainer.fast_dev_run:
        raise Exception("Cannot use wandb callbacks since pytorch lightning disables loggers in debug mode.")

    if isinstance(trainer.logger, WandbLogger):
        return trainer.logger

    if isinstance(trainer.logger, LoggerCollection):
        for logger in trainer.logger:
            if isinstance(logger, WandbLogger):
                return logger

    raise Exception(
        "You are using wandb related callback, but WandbLogger was not found for some reason..."
    )


class WatchModel(Callback):
    """Make wandb watch model at the beginning of the run."""

    def __init__(self, log: str = "gradients", log_freq: int = 100):
        self.log = log
        self.log_freq = log_freq

    def on_train_start(self, trainer, pl_module):
        logger = get_wandb_logger(trainer=trainer)
        logger.watch(model=trainer.model, log=self.log, log_freq=self.log_freq)


class DefineMetric(Callback):
    """https://github.com/wandb/client/issues/736"""

    def __init__(self, kwargs_list: list[dict]):
        self.kwargs_list = kwargs_list

    def on_train_start(self, trainer: Trainer, pl_module) -> None:
        logger = get_wandb_logger(trainer=trainer)
        experiment = logger.experiment
        for kwargs in self.kwargs_list:
            experiment.define_metric(**kwargs)


class UploadCodeAsArtifact(Callback):
    """Upload all code files to wandb as an artifact, at the beginning of the run."""

    def __init__(self, code_dir: str, use_git: bool = True):
        """

        :param code_dir:
        :param use_git: if not using git, then upload all '*.py' file
        """
        self.code_dir = code_dir
        self.use_git = use_git

    @rank_zero_only
    def on_train_start(self, trainer, pl_module):
        logger = get_wandb_logger(trainer=trainer)
        experiment = logger.experiment

        code = wandb.Artifact("project-source", type="code")

        if self.use_git:
            # get .git folder
            # https://alexwlchan.net/2020/11/a-python-function-to-ignore-a-path-with-git-info-exclude/
            git_dir_path = Path(subprocess.check_output(["git", "rev-parse", "--git-dir"]).strip().decode("utf8")).resolve()

            for path in Path(self.code_dir).rglob('*'):
                if (path.is_file()
                        and (not path.is_relative_to(git_dir_path))  # ignore files in .git
                        and (subprocess.run(['git', 'check-ignore', '-q', str(path)]).returncode == 1)):  # ignore files ignored by git
                    code.add_file(str(path), name=str(path.relative_to(self.code_dir)))

        else:
            for path in Path(self.code_dir).rglob('*.py'):
                code.add_file(str(path), name=str(path.relative_to(self.code_dir)))

        experiment.use_artifact(code)


class UploadCheckpointsAsArtifact(Callback):
    """Upload checkpoints to wandb as an artifact, at the end of run."""

    def __init__(self, ckpt_dir: str = "checkpoints/", upload_best_only: bool = False):
        self.ckpt_dir = ckpt_dir
        self.upload_best_only = upload_best_only

    @rank_zero_only
    def on_keyboard_interrupt(self, trainer, pl_module):
        self.on_train_end(trainer, pl_module)

    @rank_zero_only
    def on_train_end(self, trainer, pl_module):
        logger = get_wandb_logger(trainer=trainer)
        experiment = logger.experiment

        ckpts = wandb.Artifact("experiment-ckpts", type="checkpoints")

        if self.upload_best_only:
            ckpts.add_file(trainer.checkpoint_callback.best_model_path)
        else:
            for path in Path(self.ckpt_dir).rglob('*.ckpt'):
                ckpts.add_file(str(path))

        experiment.log_artifact(ckpts)


class UploadConfigAsArtifact(Callback):
    """Upload config to wandb as an artifact, at the beginning of run."""

    def __init__(self, upload_config_only: bool):
        """

        Args:
            upload_config_only: if upload the main config only. If false, the  also upload all the environmental config like hydra.yaml
        """
        self.upload_config_only = upload_config_only

    @rank_zero_only
    def on_train_start(self, trainer, pl_module) -> None:
        logger = get_wandb_logger(trainer=trainer)
        experiment = logger.experiment

        cfgs = wandb.Artifact("experiment-configs", type="configs")

        if self.upload_config_only:
            cfgs.add_file(f"{HydraConfig.get().output_subdir}/config.yaml")
        else:
            for path in Path(HydraConfig.get().output_subdir).rglob('*.yaml'):
                cfgs.add_file(str(path))

        experiment.use_artifact(cfgs)


class UseArtifactOnTrainStart(Callback):
    def __init__(self, artifact_name: str):
        self.artifact_name = artifact_name

    @rank_zero_only
    def on_train_start(self, trainer: Trainer, pl_module: LightningModule) -> None:
        logger = get_wandb_logger(trainer=trainer)
        experiment = logger.experiment

        experiment.use_artifact(artifact_or_name=self.artifact_name)
