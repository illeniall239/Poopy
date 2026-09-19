from typing import Callable

import numpy as np


def partial_dependence(
    predict: Callable[[np.ndarray], np.ndarray], X: np.ndarray, feature: int, grid: list[float]
) -> np.ndarray:
    """For each grid value, set column `feature` of every row to it and average the predictions."""
    raise NotImplementedError
