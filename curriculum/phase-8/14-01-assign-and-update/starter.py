import numpy as np


def assign(points: np.ndarray, centroids: np.ndarray) -> np.ndarray:
    """Index of the nearest centroid (squared Euclidean, ties to the smaller index) for each point."""
    raise NotImplementedError


def update(points: np.ndarray, labels: np.ndarray, k: int, old_centroids: np.ndarray) -> np.ndarray:
    """New (k, d) centroids as the mean of each cluster's points; an empty cluster keeps its old centroid."""
    raise NotImplementedError
