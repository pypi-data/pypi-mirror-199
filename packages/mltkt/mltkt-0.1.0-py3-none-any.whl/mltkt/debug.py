from varname import argname
from .torch.tensor import tensor_repr_wrapped as trw

def debug_var(*args, **kwargs):
    print(
        ", ".join(
            [f'{k}={trw(v)}' for k, v in zip(argname('args'), args)] + 
            [f'{k}={trw(v)}' for k, v in kwargs.items()]
        )
    )
ddd = debug_var
