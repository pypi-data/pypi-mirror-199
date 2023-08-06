import torch
from pytorch_lightning import LightningModule, Trainer, Callback
from pytorch_lightning.core.optimizer import LightningOptimizer


class LogWeightGradNorm(Callback):
    def __init__(self, log_weight_norm=False, log_grad_norm=False):
        super().__init__()
        self.log_weight_norm = log_weight_norm
        self.log_grad_norm = log_grad_norm

    @torch.no_grad()
    def on_after_backward(self, trainer: Trainer, pl_module: LightningModule) -> None:
        if self.log_weight_norm:
            weight_norm = sum([torch.sum(p ** 2) for p in pl_module.parameters()]) ** (1 / 2)
            pl_module.log('weight_norm', weight_norm, on_step=True, on_epoch=False, sync_dist=True)
        if self.log_grad_norm:
            grad_norm = sum([torch.sum(p.grad ** 2) for p in pl_module.parameters() if p.grad is not None]) ** (1 / 2)
            pl_module.log('grad_norm', grad_norm, on_step=True, on_epoch=False, sync_dist=True)

        # weight_norm = 0
        # grad_norm = 0
        #
        # optimizers = pl_module.optimizers(use_pl_optimizer=True)
        # if isinstance(optimizers, LightningOptimizer):
        #     optimizers = [optimizers]
        #
        # for optimizer in optimizers:
        #     for group in optimizer.param_groups:
        #         params = group['params']
        #
        #         if self.log_weight_norm:
        #             weight_norm += sum(torch.sum(p ** 2) for p in params)
        #         if self.log_grad_norm:
        #             grad_norm += sum(torch.sum(p.grad ** 2) for p in params if p.grad is not None)
        #
        # if self.log_weight_norm:
        #     weight_norm = weight_norm ** 0.5
        #     pl_module.log('weight_norm', weight_norm, on_step=True, on_epoch=False, sync_dist=True)
        # if self.log_grad_norm:
        #     grad_norm = grad_norm ** 0.5
        #     pl_module.log('grad_norm', grad_norm, on_step=True, on_epoch=False, sync_dist=True)
