import numpy as np


def knn_regress(train_X: np.ndarray, train_y: np.ndarray, x: np.ndarray, k: int, weighted: bool = False) -> float:
    """Mean (or inverse-distance weighted mean) of the k nearest targets, with a zero-distance guard."""
    raise NotImplementedError
