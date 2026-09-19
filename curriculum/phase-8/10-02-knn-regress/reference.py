# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import numpy as np


def knn_regress(train_X: np.ndarray, train_y: np.ndarray, x: np.ndarray, k: int, weighted: bool = False) -> float:
    train_X = np.asarray(train_X, dtype=float)
    train_y = np.asarray(train_y, dtype=float)
    x = np.asarray(x, dtype=float)
    if train_X.ndim != 2 or train_y.shape != (train_X.shape[0],) or x.shape != (train_X.shape[1],):
        raise ValueError("need train_X (n, d), train_y (n,) and x (d,)")
    if not 1 <= k <= len(train_X):
        raise ValueError("k must be between 1 and n")
    distances = np.linalg.norm(train_X - x, axis=1)
    nearest = np.argsort(distances, kind="stable")[:k]
    d = distances[nearest]
    y = train_y[nearest]
    if not weighted:
        return float(y.mean())
    exact = d == 0.0
    if exact.any():
        return float(y[exact].mean())
    weights = 1.0 / d
    return float(weights @ y / weights.sum())
