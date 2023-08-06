import math


# warmup + decay as a function
def linear_warmup_decay(t_max, t_warmup, cosine=True, linear=False):
    """Linear warmup for warmup_steps, optionally with cosine annealing or linear decay to 0 at total_steps."""
    assert not (linear and cosine)

    def fn(step):
        if step < t_warmup:
            return float(step + 1) / float(max(1, t_warmup))

        if not (cosine or linear):
            # no decay
            return 1.0

        progress = float(step - t_warmup) / float(max(1, t_max - t_warmup))
        if cosine:
            # cosine decay
            return 0.5 * (1.0 + math.cos(math.pi * progress))

        # linear decay
        return 1.0 - progress

    return fn
