# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import numpy as np


def explained_variance_ratio(X: np.ndarray, k: int) -> np.ndarray:
    X = np.asarray(X, dtype=float)
    if X.ndim != 2:
        raise ValueError("X must be 2-D")
    if not 1 <= k <= min(X.shape):
        raise ValueError("k must be between 1 and min(n, d)")
    centered = X - X.mean(axis=0)
    s = np.linalg.svd(centered, compute_uv=False)  # singular values, largest first
    variance = s**2  # proportional to the covariance eigenvalues; the 1/(n-1) cancels in the ratio
    total = variance.sum()
    if total == 0:
        raise ValueError("X has zero variance")
    return variance[:k] / total
