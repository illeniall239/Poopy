import numpy as np


def embedding_grad(indices: np.ndarray, dout: np.ndarray, vocab_size: int, dim: int) -> np.ndarray:
    """Return the (vocab_size, dim) table gradient, summing contributions of repeated indices."""
    raise NotImplementedError
