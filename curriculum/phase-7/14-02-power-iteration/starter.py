import numpy as np


def power_iteration(A: np.ndarray, n_iter: int = 1000, tol: float = 1e-12, seed: int = 0) -> tuple[float, np.ndarray]:
    """(dominant eigenvalue, unit eigenvector) of a symmetric matrix by power iteration from a seeded random start."""
    raise NotImplementedError


def top_two_eigenpairs(
    A: np.ndarray, n_iter: int = 1000
) -> tuple[tuple[float, np.ndarray], tuple[float, np.ndarray]]:
    """((λ1, v1), (λ2, v2)) via power iteration and one deflation step."""
    raise NotImplementedError
