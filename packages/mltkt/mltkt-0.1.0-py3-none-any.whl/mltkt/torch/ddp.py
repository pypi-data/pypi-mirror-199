from functools import wraps
from typing import Callable, Optional, Any
import os
import torch.distributed as dist
from ..utils.essential import static_var

# ref: https://github.com/Lightning-AI/lightning/blob/master/src/lightning/fabric/utilities/rank_zero.py 

def get_rank() -> Optional[int]:
    # fixme: this might not be the global rank
    if dist.is_initialized():
        return dist.get_rank()
    
    # SLURM_PROCID can be set even if SLURM is not managing the multiprocessing,
    # therefore LOCAL_RANK needs to be checked first
    rank_keys = ("RANK", "LOCAL_RANK", "SLURM_PROCID", "JSM_NAMESPACE_RANK")
    for key in rank_keys:
        rank = os.environ.get(key)
        if rank is not None:
            return int(rank)
    # None to differentiate whether an environment variable was set at all
    return None

@static_var(rank=get_rank() or 0)
def rank0only(fn: Callable) -> Callable:
    """Wrap a function to call internal function only in rank zero.
    Function that can be used as a decorator to enable a function/method being called only on global rank 0.
    """
    @wraps(fn)
    def wrapped_fn(*args: Any, **kwargs: Any) -> Optional[Any]:
        rank = getattr(rank0only, "rank", None)
        if rank is None:
            raise RuntimeError("The `rank0only.rank` needs to be set before use")
        if rank == 0:
            return fn(*args, **kwargs)
        return None

    return wrapped_fn
