# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
import numpy as np


def affine_lists(X: list[list[float]], W: list[list[float]], b: list[float]) -> list[list[float]]:
    d, k = len(W), len(W[0])
    if any(len(row) != d for row in X) or len(b) != k:
        raise ValueError("shape mismatch")
    cols = list(zip(*W))
    return [[float(sum(x * w for x, w in zip(row, col)) + bj) for col, bj in zip(cols, b)] for row in X]


def affine_numpy(X: np.ndarray, W: np.ndarray, b: np.ndarray) -> np.ndarray:
    if X.ndim != 2 or W.ndim != 2 or b.ndim != 1:
        raise ValueError("X and W must be 2-D and b must be 1-D")
    if X.shape[1] != W.shape[0] or b.shape[0] != W.shape[1]:
        raise ValueError("shape mismatch")
    return X @ W + b
