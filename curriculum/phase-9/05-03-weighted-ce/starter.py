import numpy as np


def weighted_ce(
    logits: np.ndarray,
    target: np.ndarray,
    class_weights: np.ndarray | None = None,
    reduction: str = "mean",
) -> float:
    """Cross-entropy from raw logits with optional class weights and "mean" or "sum" reduction, like F.cross_entropy."""
    raise NotImplementedError
