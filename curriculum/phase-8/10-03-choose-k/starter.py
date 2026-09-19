import numpy as np


def cv_accuracy(X: np.ndarray, y: np.ndarray, k: int, folds: int) -> float:
    """Mean kNN validation accuracy over contiguous, unshuffled k-fold splits."""
    raise NotImplementedError


def choose_k(X: np.ndarray, y: np.ndarray, ks: list[int], folds: int) -> int:
    """Return the k in ks with the best cross-validated accuracy, ties to the smaller k."""
    raise NotImplementedError
