import numpy as np


def knn_predict(train_X: np.ndarray, train_y: np.ndarray, x: np.ndarray, k: int) -> int:
    """Majority label of the k nearest training points, ties by nearest member then smallest label."""
    raise NotImplementedError
