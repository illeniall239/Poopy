import numpy as np


def learning_curve(fit, predict, X: np.ndarray, y: np.ndarray, sizes: list[int], folds: list) -> list[tuple[int, float, float]]:
    """(size, mean train MSE, mean validation MSE) per training size, averaged over the folds."""
    raise NotImplementedError


def more_data_helps(curve: list[tuple[int, float, float]], tol: float = 1e-3) -> bool:
    """True when the final train/validation gap is still open and still closing, by more than tol."""
    raise NotImplementedError
