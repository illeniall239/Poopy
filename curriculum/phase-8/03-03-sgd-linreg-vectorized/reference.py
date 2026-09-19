# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import numpy as np


def _check(X: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    if X.ndim != 2 or y.ndim != 1 or X.shape[0] != y.shape[0] or X.shape[0] == 0:
        raise ValueError("X must be (n, d) and y (n,) with n > 0")
    return X, y


def normal_equation(X: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, float]:
    X, y = _check(X, y)
    A = np.column_stack([np.ones(len(X)), X])
    theta = np.linalg.solve(A.T @ A, A.T @ y)
    return theta[1:], float(theta[0])


def sgd_linreg(
    X: np.ndarray, y: np.ndarray, lr: float, epochs: int, batch_size: int, seed: int
) -> tuple[np.ndarray, float, list[float]]:
    X, y = _check(X, y)
    mu = X.mean(axis=0)
    sigma = X.std(axis=0)
    if np.any(sigma == 0):
        raise ValueError("a column of X is constant")
    Z = (X - mu) / sigma

    n, d = Z.shape
    w_z = np.zeros(d)
    b_z = 0.0
    rng = np.random.default_rng(seed)
    history = []
    for _ in range(epochs):
        order = rng.permutation(n)
        for start in range(0, n, batch_size):
            idx = order[start:start + batch_size]
            err = Z[idx] @ w_z + b_z - y[idx]
            m = len(idx)
            w_z -= lr * (2.0 / m) * (Z[idx].T @ err)
            b_z -= lr * (2.0 / m) * err.sum()
        history.append(float(np.mean((Z @ w_z + b_z - y) ** 2)))

    w = w_z / sigma
    b = float(b_z - np.sum(w_z * mu / sigma))
    return w, b, history
