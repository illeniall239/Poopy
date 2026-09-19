# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import numpy as np


def softmax_loss_and_grad(
    X: np.ndarray, y: np.ndarray, W: np.ndarray, b: np.ndarray
) -> tuple[float, np.ndarray, np.ndarray]:
    X = np.asarray(X, dtype=float)
    y = np.asarray(y)
    n = X.shape[0]
    Z = X @ W + b
    Z = Z - Z.max(axis=1, keepdims=True)  # shift each row: exp now tops out at 1
    log_probs = Z - np.log(np.exp(Z).sum(axis=1, keepdims=True))
    loss = float(-log_probs[np.arange(n), y].mean())
    G = np.exp(log_probs)  # P
    G[np.arange(n), y] -= 1.0  # P - Y
    G /= n
    return loss, X.T @ G, G.sum(axis=0)


def train_softmax_regression(
    X: np.ndarray, y: np.ndarray, n_classes: int, lr: float, epochs: int
) -> tuple[np.ndarray, np.ndarray, list[float]]:
    X = np.asarray(X, dtype=float)
    y = np.asarray(y)
    if lr <= 0 or epochs < 1 or n_classes < 2:
        raise ValueError("need lr > 0, epochs >= 1 and at least two classes")
    if X.ndim != 2 or y.shape != (X.shape[0],):
        raise ValueError("X must be (n, d) and y must be (n,)")
    if np.any(y < 0) or np.any(y >= n_classes):
        raise ValueError("label out of range")
    W = np.zeros((X.shape[1], n_classes))
    b = np.zeros(n_classes)
    losses = []
    for _ in range(epochs):
        loss, dW, db = softmax_loss_and_grad(X, y, W, b)
        losses.append(loss)
        W -= lr * dW
        b -= lr * db
    return W, b, losses


def predict(X: np.ndarray, W: np.ndarray, b: np.ndarray) -> np.ndarray:
    return np.argmax(np.asarray(X, dtype=float) @ W + b, axis=1)
