# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import numpy as np


def gd_step_with_l2(w: np.ndarray, grad: np.ndarray, lr: float, lam: float) -> np.ndarray:
    w = np.asarray(w, dtype=float)
    grad = np.asarray(grad, dtype=float)
    if lam < 0 or lr <= 0:
        raise ValueError("need lam >= 0 and lr > 0")
    if w.shape != grad.shape:
        raise ValueError("w and grad must have the same shape")
    return w - lr * (grad + lam * w)


def soft_threshold(w: np.ndarray, t: float) -> np.ndarray:
    if t < 0:
        raise ValueError("t must be non-negative")
    w = np.asarray(w, dtype=float)
    return np.sign(w) * np.maximum(np.abs(w) - t, 0.0)
