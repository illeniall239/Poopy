# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import numpy as np


def _check(z, y):
    z = np.asarray(z, dtype=float)
    y = np.asarray(y, dtype=float)
    if z.shape != y.shape or z.size == 0:
        raise ValueError("z and y must be non-empty and the same shape")
    return z, y


def _sigmoid(z: np.ndarray) -> np.ndarray:
    e = np.exp(-np.abs(z))
    return np.where(z >= 0, 1.0 / (1.0 + e), e / (1.0 + e))


def bce_with_logits(z: np.ndarray, y: np.ndarray) -> float:
    z, y = _check(z, y)
    losses = np.maximum(z, 0.0) - z * y + np.log1p(np.exp(-np.abs(z)))
    return float(losses.mean())


def bce_with_logits_grad(z: np.ndarray, y: np.ndarray) -> np.ndarray:
    z, y = _check(z, y)
    return (_sigmoid(z) - y) / z.size
