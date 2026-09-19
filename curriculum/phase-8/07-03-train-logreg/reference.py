# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import numpy as np


def _sigmoid(z: np.ndarray) -> np.ndarray:
    e = np.exp(-np.abs(z))
    return np.where(z >= 0, 1.0 / (1.0 + e), e / (1.0 + e))


def _bce_from_logits(z: np.ndarray, y: np.ndarray) -> float:
    return float(np.mean(np.maximum(z, 0.0) - z * y + np.log1p(np.exp(-np.abs(z)))))


def train_logreg(X: np.ndarray, y: np.ndarray, lr: float, epochs: int) -> tuple[np.ndarray, float, list[float]]:
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    if lr <= 0 or epochs < 1:
        raise ValueError("need lr > 0 and epochs >= 1")
    if X.ndim != 2 or y.shape != (X.shape[0],):
        raise ValueError("X must be (n, d) and y must be (n,)")
    n, d = X.shape
    w = np.zeros(d)
    b = 0.0
    losses = []
    for _ in range(epochs):
        z = X @ w + b
        losses.append(_bce_from_logits(z, y))
        error = _sigmoid(z) - y
        w -= lr * (X.T @ error) / n
        b -= lr * float(error.mean())
    return w, b, losses


def predict_proba(X: np.ndarray, w: np.ndarray, b: float) -> np.ndarray:
    return _sigmoid(np.asarray(X, dtype=float) @ w + b)


def predict(X: np.ndarray, w: np.ndarray, b: float, threshold: float = 0.5) -> np.ndarray:
    return (predict_proba(X, w, b) >= threshold).astype(int)
