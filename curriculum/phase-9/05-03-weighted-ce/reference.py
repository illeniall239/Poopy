# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import numpy as np


def weighted_ce(
    logits: np.ndarray,
    target: np.ndarray,
    class_weights: np.ndarray | None = None,
    reduction: str = "mean",
) -> float:
    z = np.asarray(logits, dtype=float)
    y = np.asarray(target)
    if z.ndim != 2 or z.shape[0] == 0 or z.shape[1] == 0:
        raise ValueError("logits must be a non-empty (N, C) array")
    n, c = z.shape
    if y.shape != (n,) or not np.issubdtype(y.dtype, np.integer) or np.any((y < 0) | (y >= c)):
        raise ValueError("target must hold N class indices in 0..C-1")
    w = np.ones(c) if class_weights is None else np.asarray(class_weights, dtype=float)
    if w.shape != (c,) or np.any(w < 0):
        raise ValueError("class_weights must be C non-negative numbers")
    if reduction not in ("mean", "sum"):
        raise ValueError("reduction must be 'mean' or 'sum'")

    # stable log-sum-exp: shift each row by its max so exp never overflows
    m = z.max(axis=1, keepdims=True)
    lse = m[:, 0] + np.log(np.exp(z - m).sum(axis=1))
    nll = lse - z[np.arange(n), y]           # -log softmax(z)[y], per example
    w_y = w[y]
    total = float((w_y * nll).sum())

    if reduction == "sum":
        return total
    if w_y.sum() == 0:
        raise ValueError("weighted mean is undefined: the targets' weights sum to 0")
    return total / float(w_y.sum())
