import numpy as np


def softmax(logits: np.ndarray) -> np.ndarray:
    """Numerically stable softmax along the last axis."""
    raise NotImplementedError


def top_k_accuracy(logits_rows: np.ndarray, targets: np.ndarray, k: int) -> float:
    """Fraction of rows whose target is among the k largest logits (ties to the smaller index)."""
    raise NotImplementedError
