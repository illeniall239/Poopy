import numpy as np


def ridge_closed_form(X: np.ndarray, y: np.ndarray, lam: float) -> tuple[np.ndarray, float]:
    """Return (w, b) minimizing squared error + lam·‖w‖², with the bias b not penalized."""
    raise NotImplementedError
