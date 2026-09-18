# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import numpy as np


def replace_outliers(x: np.ndarray, k: float) -> np.ndarray:
    mean = x.mean(axis=0)
    std = x.std(axis=0)
    medians = np.median(x, axis=0)
    mask = np.abs(x - mean) > k * std
    result = x.copy()
    result[mask] = np.broadcast_to(medians, x.shape)[mask]
    return result
