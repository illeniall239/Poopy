# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import numpy as np


def power_iteration(A: np.ndarray, n_iter: int = 1000, tol: float = 1e-12, seed: int = 0) -> tuple[float, np.ndarray]:
    A = np.asarray(A, dtype=float)
    if A.ndim != 2 or A.shape[0] != A.shape[1]:
        raise ValueError("A must be a square 2-D array")
    if not np.allclose(A, A.T, atol=1e-9):
        raise ValueError("A must be symmetric")
    v = np.random.default_rng(seed).normal(size=A.shape[0])
    v /= np.linalg.norm(v)
    for _ in range(n_iter):
        w = A @ v
        norm = np.linalg.norm(w)
        if norm == 0:
            break
        w /= norm
        if np.linalg.norm(w - v) < tol:
            v = w
            break
        v = w
    return float(v @ A @ v), v


def top_two_eigenpairs(
    A: np.ndarray, n_iter: int = 1000
) -> tuple[tuple[float, np.ndarray], tuple[float, np.ndarray]]:
    lam1, v1 = power_iteration(A, n_iter)
    deflated = np.asarray(A, dtype=float) - lam1 * np.outer(v1, v1)
    lam2, v2 = power_iteration(deflated, n_iter)
    return (lam1, v1), (lam2, v2)
