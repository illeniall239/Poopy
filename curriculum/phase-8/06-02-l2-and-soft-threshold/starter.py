import numpy as np


def gd_step_with_l2(w: np.ndarray, grad: np.ndarray, lr: float, lam: float) -> np.ndarray:
    """Return w − lr·(grad + lam·w): one gradient step on loss + (lam/2)·‖w‖²."""
    raise NotImplementedError


def soft_threshold(w: np.ndarray, t: float) -> np.ndarray:
    """Return sign(w)·max(|w| − t, 0) elementwise: the L1 proximal step."""
    raise NotImplementedError
