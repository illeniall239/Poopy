# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import numpy as np


def linear_backward(X: np.ndarray, W: np.ndarray, dY: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    X, W, dY = np.asarray(X, dtype=float), np.asarray(W, dtype=float), np.asarray(dY, dtype=float)
    if X.ndim != 2 or W.ndim != 2 or dY.ndim != 2:
        raise ValueError("X, W and dY must be 2-D")
    if X.shape[1] != W.shape[0] or dY.shape != (X.shape[0], W.shape[1]):
        raise ValueError(f"shapes do not fit: X {X.shape}, W {W.shape}, dY {dY.shape}")
    dX = dY @ W.T          # (N, M) @ (M, D) -> (N, D)
    dW = X.T @ dY          # (D, N) @ (N, M) -> (D, M)
    db = dY.sum(axis=0)    # b was broadcast over the N rows
    return dX, dW, db
