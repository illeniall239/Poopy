# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import numpy as np


def softmax_ce_backward(logits: np.ndarray, targets: np.ndarray) -> tuple[float, np.ndarray]:
    z = np.asarray(logits, dtype=float)
    y = np.asarray(targets)
    if z.ndim != 2 or z.shape[0] == 0:
        raise ValueError("logits must be a non-empty (N, C) array")
    n, c = z.shape
    if y.shape != (n,) or not np.issubdtype(y.dtype, np.integer) or np.any((y < 0) | (y >= c)):
        raise ValueError("targets must be N integers in 0..C-1")
    shifted = z - z.max(axis=1, keepdims=True)
    log_probs = shifted - np.log(np.exp(shifted).sum(axis=1, keepdims=True))
    rows = np.arange(n)
    loss = -log_probs[rows, y].mean()
    dlogits = np.exp(log_probs)
    dlogits[rows, y] -= 1.0
    return float(loss), dlogits / n
