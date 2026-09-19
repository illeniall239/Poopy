import numpy as np


def bce_with_logits(z: np.ndarray, y: np.ndarray) -> float:
    """Mean binary cross-entropy computed stably from logits z and labels y."""
    raise NotImplementedError


def bce_with_logits_grad(z: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Gradient of the mean BCE with respect to z: (sigmoid(z) - y) / n."""
    raise NotImplementedError
