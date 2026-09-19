import numpy as np


def cosine_lr(step: int, total: int, base: float, warmup: int) -> float:
    """Learning rate with linear warmup from 0 to base, then cosine decay to 0 at step == total."""
    raise NotImplementedError


def clip_grad_norm(grads: list[np.ndarray], max_norm: float) -> float:
    """Scale all grads in place so their global L2 norm is at most max_norm; return the norm before clipping."""
    raise NotImplementedError
