import numpy as np


def affine_lists(X: list[list[float]], W: list[list[float]], b: list[float]) -> list[list[float]]:
    """X (n×d) times W (d×k) plus bias b (k) as a list of rows; ValueError on shape mismatch."""
    raise NotImplementedError


def affine_numpy(X: np.ndarray, W: np.ndarray, b: np.ndarray) -> np.ndarray:
    """X @ W + b with broadcasting, shape (n, k); ValueError on shape mismatch or a non-1-D b."""
    raise NotImplementedError
