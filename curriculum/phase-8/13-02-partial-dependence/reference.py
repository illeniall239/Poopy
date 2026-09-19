# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
from typing import Callable

import numpy as np


def partial_dependence(
    predict: Callable[[np.ndarray], np.ndarray], X: np.ndarray, feature: int, grid: list[float]
) -> np.ndarray:
    X = np.asarray(X, dtype=float)
    if X.ndim != 2 or len(X) == 0:
        raise ValueError("X must be a non-empty 2-D array")
    if not 0 <= feature < X.shape[1]:
        raise ValueError("feature index out of range")
    averages = []
    for value in grid:
        edited = X.copy()
        edited[:, feature] = value  # every row gets this value; the other columns stay as they are
        averages.append(np.mean(predict(edited)))
    return np.array(averages, dtype=float)
