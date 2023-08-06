from torch import nn
import contextlib
from typing import Optional

def compute_gradient_norm_stat(model: nn.Module):
    grad_norm = 0
    for p in model.parameters():
        if p.grad is not None:
            grad_norm += (p.grad.data ** 2).sum().item()
    return grad_norm


def compute_weight_norm_stat(model: nn.Module):
    weight_norm = 0
    for p in model.parameters():
        if p.data is not None:
            weight_norm += (p.data ** 2).sum().item()
    return weight_norm

@contextlib.contextmanager
def set_training(model: nn.Module, mode: Optional[bool] = None):
    if mode is None:
        yield
        return
    old_mode = model.training
    if old_mode != mode:
        model.train(mode)
    try:
        yield
    finally:
        if old_mode != mode:
            model.train(old_mode)

