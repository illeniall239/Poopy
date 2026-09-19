# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import math

import numpy as np


def cosine_lr(step: int, total: int, base: float, warmup: int) -> float:
    if not 0 <= step <= total or base <= 0 or not 0 <= warmup < total:
        raise ValueError("need 0 <= step <= total, base > 0 and 0 <= warmup < total")
    if step < warmup:
        return base * step / warmup
    progress = (step - warmup) / (total - warmup)
    return base * 0.5 * (1 + math.cos(math.pi * progress))


def clip_grad_norm(grads: list[np.ndarray], max_norm: float) -> float:
    if max_norm <= 0:
        raise ValueError("max_norm must be positive")
    norm = math.sqrt(sum(float(np.sum(g * g)) for g in grads))
    if norm > max_norm:
        scale = max_norm / norm
        for g in grads:
            g *= scale
    return norm
