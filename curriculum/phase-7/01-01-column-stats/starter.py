import numpy as np


def column_stats(x: np.ndarray) -> dict[str, np.ndarray]:
    """Return {"mean", "std", "min", "max"} per column of a 2-D array, each of shape (n_cols,), with no Python loops."""
    raise NotImplementedError
