# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
from itertools import combinations
from math import factorial
from typing import Callable

import numpy as np


def shapley_values(
    predict: Callable[[np.ndarray], np.ndarray], x: np.ndarray, background: np.ndarray
) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    background = np.asarray(background, dtype=float)
    if x.ndim != 1 or x.shape != background.shape:
        raise ValueError("x and background must be 1-D arrays of the same length")
    d = len(x)
    if not 1 <= d <= 4:
        raise ValueError("exact enumeration is limited to 1 to 4 features")

    def value(coalition: tuple[int, ...]) -> float:
        # Features in the coalition take x's value, the rest keep the background's.
        z = background.copy()
        z[list(coalition)] = x[list(coalition)]
        return float(predict(z[None, :])[0])

    phi = np.zeros(d)
    for i in range(d):
        others = [j for j in range(d) if j != i]
        for size in range(d):
            weight = factorial(size) * factorial(d - size - 1) / factorial(d)
            for coalition in combinations(others, size):
                phi[i] += weight * (value(coalition + (i,)) - value(coalition))
    return phi
