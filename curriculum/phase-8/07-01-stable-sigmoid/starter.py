import numpy as np


def stable_sigmoid(z: float) -> float:
    """Return 1 / (1 + e^-z) without overflow for any float z."""
    raise NotImplementedError


def stable_sigmoid_np(z: np.ndarray) -> np.ndarray:
    """Elementwise sigmoid of an array, with no overflow warnings."""
    raise NotImplementedError
