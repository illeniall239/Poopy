import numpy as np


def softmax_ce_backward(logits: np.ndarray, targets: np.ndarray) -> tuple[float, np.ndarray]:
    """Mean softmax cross-entropy over the batch and its gradient with respect to the logits."""
    raise NotImplementedError
