import numpy as np


def low_rank(X: np.ndarray, k: int) -> np.ndarray:
    """Best rank-k approximation of X from its SVD; ValueError if k is out of range."""
    raise NotImplementedError


def reconstruction_error(X: np.ndarray, k: int) -> float:
    """Frobenius norm of X - low_rank(X, k)."""
    raise NotImplementedError


def explained_variance(X: np.ndarray, k: int) -> float:
    """Fraction of variance kept by the first k principal components of the column-centered X."""
    raise NotImplementedError
