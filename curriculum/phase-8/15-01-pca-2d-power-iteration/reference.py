# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import numpy as np


def power_iteration(A: np.ndarray, n_iter: int = 10000, tol: float = 1e-12, seed: int = 0) -> tuple[float, np.ndarray]:
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


def pca_2d(points: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    points = np.asarray(points, dtype=float)
    if points.ndim != 2 or points.shape[0] < 2 or points.shape[1] < 2:
        raise ValueError("need a 2-D array with at least 2 rows and 2 columns")
    centered = points - points.mean(axis=0)  # PCA describes spread around the mean, not around the origin
    cov = centered.T @ centered / (len(points) - 1)
    lam1, v1 = power_iteration(cov)
    lam2, v2 = power_iteration(cov - lam1 * np.outer(v1, v1))  # deflation removes the first direction
    return np.vstack([v1, v2]), np.array([lam1, lam2])
