import numpy as np


def reconstruction_errors(X_train: np.ndarray, X: np.ndarray, n_components: int) -> np.ndarray:
    """Squared error of reconstructing each row of X from the top PCA components of X_train."""
    raise NotImplementedError


def top_anomalies(errors: np.ndarray, n: int) -> list[int]:
    """Indices of the n largest errors, largest first, lower index first on ties."""
    raise NotImplementedError
