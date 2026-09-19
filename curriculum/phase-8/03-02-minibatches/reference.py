# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
from typing import Iterator

import numpy as np


def minibatches(n: int, batch_size: int, rng: np.random.Generator) -> Iterator[list[int]]:
    # Not a generator itself, so bad arguments fail at the call, not at the first next().
    if n < 0:
        raise ValueError("n must be >= 0")
    if batch_size < 1:
        raise ValueError("batch_size must be >= 1")
    order = rng.permutation(n).tolist()
    return (order[start:start + batch_size] for start in range(0, n, batch_size))
