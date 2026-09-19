# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import numpy as np


def assign(points: np.ndarray, centroids: np.ndarray) -> np.ndarray:
    points = np.asarray(points, dtype=float)
    centroids = np.asarray(centroids, dtype=float)
    if points.ndim != 2 or centroids.ndim != 2 or points.shape[1] != centroids.shape[1] or len(centroids) == 0:
        raise ValueError("points (n, d) and centroids (k, d) must share d, with k >= 1")
    # (n, k) squared distances by broadcasting; argmin returns the first (smallest) index on a tie.
    distances = ((points[:, None, :] - centroids[None, :, :]) ** 2).sum(axis=2)
    return distances.argmin(axis=1)


def update(points: np.ndarray, labels: np.ndarray, k: int, old_centroids: np.ndarray) -> np.ndarray:
    points = np.asarray(points, dtype=float)
    labels = np.asarray(labels)
    old_centroids = np.asarray(old_centroids, dtype=float)
    if len(labels) != len(points) or old_centroids.shape != (k, points.shape[1]):
        raise ValueError("labels must match points and old_centroids must have shape (k, d)")
    if len(labels) and (labels.min() < 0 or labels.max() >= k):
        raise ValueError("labels must be in range(k)")
    new = old_centroids.copy()
    for c in range(k):
        members = points[labels == c]
        if len(members):  # an empty cluster keeps its old centroid instead of becoming NaN
            new[c] = members.mean(axis=0)
    return new
