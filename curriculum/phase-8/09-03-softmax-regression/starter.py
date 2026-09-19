import numpy as np


def softmax_loss_and_grad(
    X: np.ndarray, y: np.ndarray, W: np.ndarray, b: np.ndarray
) -> tuple[float, np.ndarray, np.ndarray]:
    """Return (mean cross-entropy, dW, db) for logits X W + b and integer labels y."""
    raise NotImplementedError


def train_softmax_regression(
    X: np.ndarray, y: np.ndarray, n_classes: int, lr: float, epochs: int
) -> tuple[np.ndarray, np.ndarray, list[float]]:
    """Full-batch gradient descent from zeros; return (W, b, per-epoch losses)."""
    raise NotImplementedError


def predict(X: np.ndarray, W: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Return the argmax class of X W + b for every row."""
    raise NotImplementedError
