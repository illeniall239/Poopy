# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import numpy as np


def softmax(logits: np.ndarray) -> np.ndarray:
    z = np.asarray(logits, dtype=float)
    shifted = z - z.max(axis=-1, keepdims=True)
    e = np.exp(shifted)
    return e / e.sum(axis=-1, keepdims=True)


def top_k_accuracy(logits_rows: np.ndarray, targets: np.ndarray, k: int) -> float:
    z = np.asarray(logits_rows, dtype=float)
    targets = np.asarray(targets)
    if z.ndim != 2:
        raise ValueError("logits_rows must be 2-D (n, C)")
    n, c = z.shape
    if targets.shape != (n,):
        raise ValueError("need one target per row")
    if not 1 <= k <= c:
        raise ValueError("k must be between 1 and the number of classes")
    if np.any(targets < 0) or np.any(targets >= c):
        raise ValueError("target out of range")
    target_logit = z[np.arange(n), targets][:, None]
    smaller_index = np.arange(c)[None, :] < targets[:, None]
    rank = np.sum((z > target_logit) | ((z == target_logit) & smaller_index), axis=1)
    return float(np.mean(rank < k))
