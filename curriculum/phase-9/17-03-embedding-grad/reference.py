# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import numpy as np


def embedding_grad(indices: np.ndarray, dout: np.ndarray, vocab_size: int, dim: int) -> np.ndarray:
    indices = np.asarray(indices)
    dout = np.asarray(dout, dtype=float)
    if dout.shape != indices.shape + (dim,):
        raise ValueError("dout must have shape indices.shape + (dim,)")
    if indices.size and (indices.min() < 0 or indices.max() >= vocab_size):
        raise ValueError("index out of range")
    grad = np.zeros((vocab_size, dim))
    # np.add.at is unbuffered: every occurrence of a repeated index adds its row.
    np.add.at(grad, indices.reshape(-1), dout.reshape(-1, dim))
    return grad
