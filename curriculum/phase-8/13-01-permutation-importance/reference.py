# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
from typing import Callable

import numpy as np


def permutation_importance(
    predict: Callable[[np.ndarray], np.ndarray],
    X: np.ndarray,
    y: np.ndarray,
    metric: Callable[[np.ndarray, np.ndarray], float],
    rng: np.random.Generator,
    repeats: int = 5,
) -> np.ndarray:
    if repeats < 1:
        raise ValueError("repeats must be at least 1")
    X = np.asarray(X, dtype=float)
    if X.ndim != 2 or len(X) != len(y):
        raise ValueError("X must be 2-D with one row per label")
    baseline = metric(y, predict(X))
    importances = np.zeros(X.shape[1])
    for j in range(X.shape[1]):
        drops = []
        for _ in range(repeats):
            shuffled = X.copy()  # never touch the caller's X
            shuffled[:, j] = rng.permutation(X[:, j])
            drops.append(baseline - metric(y, predict(shuffled)))
        importances[j] = np.mean(drops)
    return importances
