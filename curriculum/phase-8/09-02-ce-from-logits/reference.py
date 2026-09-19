# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import numpy as np


def log_softmax(logits: np.ndarray) -> np.ndarray:
    z = np.asarray(logits, dtype=float)
    m = z.max(axis=-1, keepdims=True)
    logsumexp = m + np.log(np.exp(z - m).sum(axis=-1, keepdims=True))
    return z - logsumexp


def cross_entropy_from_logits(logits: np.ndarray, target_idx) -> float:
    z = np.asarray(logits, dtype=float)
    if z.ndim == 1:
        z = z[None, :]
        targets = np.array([target_idx])
    elif z.ndim == 2:
        targets = np.asarray(target_idx)
    else:
        raise ValueError("logits must be 1-D or 2-D")
    n, c = z.shape
    if targets.shape != (n,):
        raise ValueError("need one target per row")
    if np.any(targets < 0) or np.any(targets >= c):
        raise ValueError("target out of range")
    return float(-log_softmax(z)[np.arange(n), targets].mean())
