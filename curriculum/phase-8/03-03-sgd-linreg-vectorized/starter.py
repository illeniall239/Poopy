import numpy as np


def normal_equation(X: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, float]:
    """Least-squares (w, b) by solving (AᵀA)θ = Aᵀy with A = [1 | X]."""
    raise NotImplementedError


def sgd_linreg(
    X: np.ndarray, y: np.ndarray, lr: float, epochs: int, batch_size: int, seed: int
) -> tuple[np.ndarray, float, list[float]]:
    """Minibatch SGD on standardized features; returns (w, b) in original units and per-epoch MSE."""
    raise NotImplementedError
