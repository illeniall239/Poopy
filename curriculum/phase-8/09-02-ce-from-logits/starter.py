import numpy as np


def log_softmax(logits: np.ndarray) -> np.ndarray:
    """Return z - logsumexp(z) along the last axis, computed stably."""
    raise NotImplementedError


def cross_entropy_from_logits(logits: np.ndarray, target_idx) -> float:
    """Return -log softmax(logits)[target] for one row, or the mean over a batch of rows."""
    raise NotImplementedError
