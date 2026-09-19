# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import numpy as np


def ridge_closed_form(X: np.ndarray, y: np.ndarray, lam: float) -> tuple[np.ndarray, float]:
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    if lam < 0:
        raise ValueError("lam must be non-negative")
    if X.ndim != 2 or y.shape != (X.shape[0],):
        raise ValueError("X must be (n, d) and y must be (n,)")
    x_mean = X.mean(axis=0)
    y_mean = y.mean()
    Xc = X - x_mean
    yc = y - y_mean
    d = X.shape[1]
    w = np.linalg.solve(Xc.T @ Xc + lam * np.eye(d), Xc.T @ yc)
    b = float(y_mean - x_mean @ w)
    return w, b
