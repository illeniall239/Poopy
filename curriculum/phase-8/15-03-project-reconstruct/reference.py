# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import numpy as np


def project(X: np.ndarray, k: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    X = np.asarray(X, dtype=float)
    if X.ndim != 2:
        raise ValueError("X must be 2-D")
    if not 1 <= k <= min(X.shape):
        raise ValueError("k must be between 1 and min(n, d)")
    mean = X.mean(axis=0)
    centered = X - mean
    _, _, Vt = np.linalg.svd(centered, full_matrices=False)
    components = Vt[:k]  # rows are unit directions, largest variance first
    Z = centered @ components.T
    return Z, components, mean


def reconstruct(Z: np.ndarray, components: np.ndarray, mean: np.ndarray) -> np.ndarray:
    Z = np.asarray(Z, dtype=float)
    components = np.asarray(components, dtype=float)
    if Z.ndim != 2 or components.ndim != 2 or Z.shape[1] != components.shape[0] or components.shape[1] != len(mean):
        raise ValueError("need Z (n, k), components (k, d) and mean (d,)")
    return Z @ components + mean
