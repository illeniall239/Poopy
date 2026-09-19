import numpy as np


def unbroadcast(grad: np.ndarray, shape: tuple[int, ...]) -> np.ndarray:
    """Sum grad back down to the shape it was broadcast from."""
    raise NotImplementedError
