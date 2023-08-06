import torch
from torch import Tensor


def nuclear_norm(X: Tensor, bias: bool):
    assert len(X.shape) == 2

    if bias:
        X = torch.column_stack([X, torch.ones((X.shape[0], 1)).type_as(X)])

    return torch.linalg.norm(X, ord='nuc')


def normalized_rank(X: Tensor, bias: bool, eps=1e-9):
    assert len(X.shape) == 2

    if bias:
        X = torch.column_stack([X, torch.ones((X.shape[0], 1)).type_as(X)])

    nuc_norm = torch.linalg.norm(X, ord='nuc')
    induced_norm = torch.clamp(torch.linalg.norm(X, ord=2), min=eps)
    max_rank = min(*X.shape)

    return nuc_norm / induced_norm / max_rank


def normalized_rank_fro(X: Tensor, bias, eps=1e-9):
    assert len(X.shape) == 2

    if bias:
        X = torch.column_stack([X, torch.ones((X.shape[0], 1)).type_as(X)])

    nuc_norm = torch.linalg.norm(X, ord='nuc')
    fro_norm = torch.clamp(torch.linalg.norm(X, ord='fro'), min=eps)
    max_rank = min(*X.shape)

    return (nuc_norm / fro_norm) ** 2 / max_rank
