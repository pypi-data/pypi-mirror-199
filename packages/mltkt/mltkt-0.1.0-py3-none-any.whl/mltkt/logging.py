import structlog
import numpy as np
import torch as th
from typing import Optional, TextIO

import logging

from .torch.tensor import tensor_repr
from .torch.ddp import get_rank
from .utils.essential import static_var


def tensor_render(logger, method_name, event_dict):
    if event_dict is not None:
        event_dict.update({
            k: tensor_repr(v) for k, v in event_dict.items()
            if isinstance(v, (th.Tensor, np.ndarray))
        })
    return event_dict


@static_var(rank=get_rank() or 0)
def drop_on_non_rank_zero(logger, method_name, event_dict):
    if drop_on_non_rank_zero.rank != 0:
        raise structlog.DropEvent
    return event_dict


shared_processors = [
    tensor_render,
    structlog.processors.CallsiteParameterAdder({
        structlog.processors.CallsiteParameter.FILENAME,
        structlog.processors.CallsiteParameter.FUNC_NAME,
        structlog.processors.CallsiteParameter.LINENO,
    }),
    structlog.processors.StackInfoRenderer(),
    structlog.dev.set_exc_info,
    structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=False),
    structlog.dev.ConsoleRenderer(),
]


def get_std_logger(name: Optional[str] = __name__, **initial_values):
    processors = [
        drop_on_non_rank_zero,
        structlog.stdlib.filter_by_level,
        structlog.contextvars.merge_contextvars,

        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
    ] + shared_processors

    return structlog.stdlib.BoundLogger(
        logging.getLogger(name),
        processors=processors,
        context=initial_values
    )


def get_print_logger(file: Optional[TextIO] = None, min_level: int = logging.NOTSET, **initial_values):
    processors = [
        drop_on_non_rank_zero,
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
    ] + shared_processors

    return structlog.make_filtering_bound_logger(min_level)(
        structlog.PrintLogger(file),
        processors=processors,
        context=initial_values
    )
