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
    """Mean drop in metric(y, predict(X)) when each column is shuffled, one value per feature."""
    raise NotImplementedError
