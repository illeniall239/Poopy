from typing import Iterator

import numpy as np


def minibatches(n: int, batch_size: int, rng: np.random.Generator) -> Iterator[list[int]]:
    """Yield shuffled index batches covering 0..n-1 exactly once, last batch possibly short."""
    raise NotImplementedError
