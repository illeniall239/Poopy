import numpy as np


def expected_initial_ce(num_classes: int) -> float:
    """Cross-entropy of a uniform prediction over num_classes classes: -log(1/C)."""
    raise NotImplementedError


def too_confident_at_init(logits: np.ndarray, tol: float) -> bool:
    """True if the label-averaged cross-entropy of these initial logits exceeds log C by more than tol."""
    raise NotImplementedError
