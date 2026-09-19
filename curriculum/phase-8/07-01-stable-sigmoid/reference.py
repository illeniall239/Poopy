# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import math

import numpy as np


def stable_sigmoid(z: float) -> float:
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    e = math.exp(z)
    return e / (1.0 + e)


def stable_sigmoid_np(z: np.ndarray) -> np.ndarray:
    z = np.asarray(z, dtype=float)
    e = np.exp(-np.abs(z))  # always in (0, 1]: never overflows
    return np.where(z >= 0, 1.0 / (1.0 + e), e / (1.0 + e))
