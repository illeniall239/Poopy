# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import numpy as np


def pairwise_distances(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    if a.shape[1] != b.shape[1]:
        raise ValueError(f"dimension mismatch: {a.shape[1]} vs {b.shape[1]}")
    diff = a[:, np.newaxis, :] - b[np.newaxis, :, :]
    return np.sqrt((diff ** 2).sum(axis=2))
