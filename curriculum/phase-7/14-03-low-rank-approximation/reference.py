# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
import numpy as np


def _check_k(X: np.ndarray, k: int) -> None:
    if k < 1 or k > min(X.shape):
        raise ValueError("k must be between 1 and min(X.shape)")


def low_rank(X: np.ndarray, k: int) -> np.ndarray:
    X = np.asarray(X, dtype=float)
    _check_k(X, k)
    U, s, Vt = np.linalg.svd(X, full_matrices=False)
    return (U[:, :k] * s[:k]) @ Vt[:k, :]


def reconstruction_error(X: np.ndarray, k: int) -> float:
    X = np.asarray(X, dtype=float)
    return float(np.linalg.norm(X - low_rank(X, k)))


def explained_variance(X: np.ndarray, k: int) -> float:
    X = np.asarray(X, dtype=float)
    _check_k(X, k)
    centered = X - X.mean(axis=0)
    s = np.linalg.svd(centered, compute_uv=False)
    total = float((s**2).sum())
    return 1.0 if total == 0 else float((s[:k] ** 2).sum() / total)
