from contextlib import contextmanager
from typing import Optional, Sequence, Tuple, Union, Dict, Any

import torch
from pl_bolts.models.self_supervised.evaluator import SSLEvaluator
from pytorch_lightning import Callback, LightningModule, Trainer
from pytorch_lightning.utilities import rank_zero_warn
from torch import Tensor
from torch import nn
from torch.nn import functional as F
from torch.optim import Optimizer
from torchmetrics.functional import accuracy


class SSLOnlineEvaluator(Callback):  # pragma: no cover
    """
    Attaches a MLP for fine-tuning using the standard self-supervised protocol.
    """

    def __init__(
            self,
            drop_p: float = 0.2,
            hidden_dim: Optional[int] = None,
    ):
        """
        Args:
            drop_p: Dropout probability
            hidden_dim: Hidden dimension for the fine-tune MLP
        """
        super().__init__()

        self.hidden_dim = hidden_dim
        self.drop_p = drop_p

        self.optimizer: Optional[Optimizer] = None
        self.online_evaluator: Optional[SSLEvaluator] = None
        self.z_dim: Optional[int] = None
        self.num_classes: Optional[int] = None
        self.dataset: Optional[str] = None

        self._recovered_callback_state: Optional[Dict[str, Any]] = None  # store the callback state in case of resuming

    def on_fit_start(self, trainer: Trainer, pl_module: LightningModule) -> None:
        self.z_dim = pl_module.online_network.backbone.fc_in_features
        self.num_classes = trainer.datamodule.num_classes
        self.dataset = trainer.datamodule.name

    def on_pretrain_routine_start(self, trainer: Trainer, pl_module: LightningModule) -> None:
        # must move to device after setup, as during setup, pl_module is still on cpu
        self.online_evaluator = SSLEvaluator(
            n_input=self.z_dim,
            n_classes=self.num_classes,
            p=self.drop_p,
            n_hidden=self.hidden_dim,
        ).to(pl_module.device)

        if trainer.accelerator_connector.is_distributed:
            if trainer.accelerator_connector.use_ddp:
                from torch.nn.parallel import DistributedDataParallel as DDP
                self.online_evaluator = torch.nn.SyncBatchNorm.convert_sync_batchnorm(self.online_evaluator)
                self.online_evaluator = DDP(self.online_evaluator, device_ids=[pl_module.device])
            elif trainer.accelerator_connector.use_dp:
                from torch.nn.parallel import DataParallel as DP
                self.online_evaluator = DP(self.online_evaluator, device_ids=[pl_module.device])
            else:
                rank_zero_warn("Does not support this type of distributed accelerator. The online evaluator will not sync.")

        self.optimizer = torch.optim.Adam(self.online_evaluator.parameters(), lr=1e-4)

        if self._recovered_callback_state is not None:
            self.online_evaluator.load_state_dict(self._recovered_callback_state['state_dict'])
            self.optimizer.load_state_dict(self._recovered_callback_state['optimizer_state'])

    def to_device(self, batch: Sequence, device: Union[str, torch.device]) -> Tuple[Tensor, Tensor]:
        # get the labeled batch
        if self.dataset == 'stl10':
            labeled_batch = batch[1]
            batch = labeled_batch

        inputs, y = batch

        # last input is for online eval
        x = inputs[-1]
        x = x.to(device)
        y = y.to(device)

        return x, y

    def shared_step(
            self,
            pl_module: LightningModule,
            batch: Sequence,
    ):

        with torch.no_grad():
            with set_training(pl_module, False):
                x, y = self.to_device(batch, pl_module.device)
                representations = pl_module(x).flatten(start_dim=1)

        # forward pass
        mlp_logits = self.online_evaluator(representations)  # type: ignore[operator]
        mlp_loss = F.cross_entropy(mlp_logits, y)

        acc = accuracy(mlp_logits.softmax(-1), y)

        return acc, mlp_loss

    def on_train_batch_end(
            self,
            trainer: Trainer,
            pl_module: LightningModule,
            outputs: Sequence,
            batch: Sequence,
            batch_idx: int,
            dataloader_idx: int,
    ) -> None:
        train_acc, mlp_loss = self.shared_step(pl_module, batch)

        # update finetune weights
        mlp_loss.backward()
        self.optimizer.step()
        self.optimizer.zero_grad()

        pl_module.log('online_train_acc', train_acc, on_step=True, on_epoch=False)
        pl_module.log('online_train_loss', mlp_loss, on_step=True, on_epoch=False)

    def on_validation_batch_end(
            self,
            trainer: Trainer,
            pl_module: LightningModule,
            outputs: Sequence,
            batch: Sequence,
            batch_idx: int,
            dataloader_idx: int,
    ) -> None:
        val_acc, mlp_loss = self.shared_step(pl_module, batch)
        pl_module.log('online_val_acc', val_acc, on_step=False, on_epoch=True, sync_dist=True)
        pl_module.log('online_val_loss', mlp_loss, on_step=False, on_epoch=True, sync_dist=True)

    def on_save_checkpoint(
            self,
            trainer: Trainer,
            pl_module: LightningModule,
            checkpoint: Dict[str, Any]
    ) -> dict:
        return {
            'state_dict': self.online_evaluator.state_dict(),
            'optimizer_state': self.optimizer.state_dict()
        }

    def on_load_checkpoint(
            self,
            trainer: Trainer,
            pl_module: LightningModule,
            callback_state: Dict[str, Any]
    ) -> None:
        # on_load_checkpoint() is called before setup() and on_pretrain_routine_start().
        # Thus, must first cache the state_dict and load it later.
        self._recovered_callback_state = callback_state


@contextmanager
def set_training(module: nn.Module, mode: bool):
    """Context manager to set training mode. When exit, recover the original training mode.
    Args:
        module: module to set training mode
        mode: whether to set training mode (True) or evaluation mode (False).
    """
    original_mode = module.training

    try:
        module.train(mode)
        yield module
    finally:
        module.train(original_mode)
