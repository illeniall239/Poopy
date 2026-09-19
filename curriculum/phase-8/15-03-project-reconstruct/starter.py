import numpy as np


def project(X: np.ndarray, k: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return (Z (n, k) coordinates, components (k, d), mean (d,)) of X on its top k principal components."""
    raise NotImplementedError


def reconstruct(Z: np.ndarray, components: np.ndarray, mean: np.ndarray) -> np.ndarray:
    """Map k-dimensional coordinates back to the original d columns: Z @ components + mean."""
    raise NotImplementedError
