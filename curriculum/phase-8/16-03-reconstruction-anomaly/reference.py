# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import numpy as np


def reconstruction_errors(X_train: np.ndarray, X: np.ndarray, n_components: int) -> np.ndarray:
    X_train = np.asarray(X_train, dtype=float)
    X = np.asarray(X, dtype=float)
    if X_train.ndim != 2 or X.ndim != 2 or X_train.shape[1] != X.shape[1]:
        raise ValueError("X_train and X must be 2-D with the same number of columns")
    if not 1 <= n_components <= X_train.shape[1]:
        raise ValueError("n_components must be between 1 and the number of features")
    mean = X_train.mean(axis=0)
    _, _, vt = np.linalg.svd(X_train - mean, full_matrices=False)
    W = vt[:n_components]  # rows are the top principal directions
    centered = X - mean
    reconstructed = (centered @ W.T) @ W
    return np.sum((centered - reconstructed) ** 2, axis=1)


def top_anomalies(errors: np.ndarray, n: int) -> list[int]:
    order = np.argsort(-np.asarray(errors, dtype=float), kind="stable")
    return order[:n].tolist()
