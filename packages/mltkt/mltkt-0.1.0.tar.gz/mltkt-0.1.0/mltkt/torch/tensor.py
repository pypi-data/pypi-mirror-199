from typing import Any, Iterable, NamedTuple, Union

import numpy as np
import torch
import yaml

def tensor_repr(T: Union[torch.Tensor, np.ndarray], numel_limit=9) -> str:
    if np.prod(T.shape) <= numel_limit:
        return repr(T)
    return f'{"x".join(str(d) for d in T.shape)} ({T.min() :.4g}, {T.max() :.4g})'

def tensor_repr_wrapped(T: Any, numel_limit=9) -> str:
    if isinstance(T, (torch.Tensor, np.ndarray)):
        return tensor_repr(T, numel_limit)
    return repr(T)

def print_tensor_collection(tensor_collection) -> None:
    def _rec(T):
        if isinstance(T, (torch.Tensor, np.ndarray)):
            return tensor_repr(T)
        elif isinstance(T, dict):
            return {k: _rec(v) for k, v in T.items()}
        elif isinstance(T, NamedTuple):
            return {k: _rec(v) for k, v in T._asdict().items()}
        elif isinstance(T, Iterable):
            return [_rec(v) for v in T]
        else:
            return str(T)

    str_rep = _rec(tensor_collection)
    
    print(yaml.dump(str_rep))
ptc = print_tensor_collection


def sanitize(t: torch.Tensor):
    t[torch.isnan(t)] = 0
    t[torch.isinf(t)] = 0
    # clean up
    return t


def raise_nan(t: torch.Tensor):
    if torch.any(torch.isnan(t)):
        raise ValueError("NaN encountered!")


def detorch(t: Union[torch.Tensor, Any]) -> Union[int, float, np.ndarray]:
    """
    ensure t is no longer a tensor, convert it to a numpy array, int or float
    """
    n = t.detach().clone().cpu().numpy() if isinstance(t, torch.Tensor) else t

    if isinstance(n, np.ndarray) and n.size == 1:
        n = n.item()

    return n


def tensor2device(tensor_tree, device: torch.device) -> None:
    def _rec(T):
        if isinstance(T, torch.Tensor):
            T.to(device)
        elif isinstance(T, dict):
            list(map(_rec, T.values()))
        elif isinstance(T, Iterable):
            list(map(_rec, T))

    _rec(tensor_tree)


t2d = tensor2device
