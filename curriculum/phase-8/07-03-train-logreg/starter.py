import numpy as np


def train_logreg(X: np.ndarray, y: np.ndarray, lr: float, epochs: int) -> tuple[np.ndarray, float, list[float]]:
    """Full-batch gradient descent on mean BCE from zeros; return (w, b, per-epoch losses)."""
    raise NotImplementedError


def predict_proba(X: np.ndarray, w: np.ndarray, b: float) -> np.ndarray:
    """Return sigmoid(X w + b) for every row."""
    raise NotImplementedError


def predict(X: np.ndarray, w: np.ndarray, b: float, threshold: float = 0.5) -> np.ndarray:
    """Return 1 where the predicted probability is >= threshold, else 0."""
    raise NotImplementedError
