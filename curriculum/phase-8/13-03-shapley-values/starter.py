from typing import Callable

import numpy as np


def shapley_values(
    predict: Callable[[np.ndarray], np.ndarray], x: np.ndarray, background: np.ndarray
) -> np.ndarray:
    """Exact Shapley value of each feature of x against one background row, by enumerating coalitions."""
    raise NotImplementedError
