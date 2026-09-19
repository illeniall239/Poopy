# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import math

import numpy as np


def expected_initial_ce(num_classes: int) -> float:
    if num_classes < 2:
        raise ValueError("need at least 2 classes")
    return math.log(num_classes)


def too_confident_at_init(logits: np.ndarray, tol: float) -> bool:
    z = np.asarray(logits, dtype=float)
    if z.ndim != 2 or z.shape[0] == 0 or z.shape[1] < 2 or tol < 0:
        raise ValueError("logits must be (N, C) with N >= 1, C >= 2, and tol >= 0")
    top = z.max(axis=1)
    logsumexp = top + np.log(np.exp(z - top[:, None]).sum(axis=1))
    loss = float(np.mean(logsumexp - z.mean(axis=1)))
    return loss > expected_initial_ce(z.shape[1]) + tol
