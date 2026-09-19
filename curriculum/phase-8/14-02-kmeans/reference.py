# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import numpy as np


def assign(points: np.ndarray, centroids: np.ndarray) -> np.ndarray:
    distances = ((points[:, None, :] - centroids[None, :, :]) ** 2).sum(axis=2)
    return distances.argmin(axis=1)


def update(points: np.ndarray, labels: np.ndarray, k: int, old_centroids: np.ndarray) -> np.ndarray:
    new = old_centroids.copy()
    for c in range(k):
        members = points[labels == c]
        if len(members):
            new[c] = members.mean(axis=0)
    return new


def inertia(points: np.ndarray, labels: np.ndarray, centroids: np.ndarray) -> float:
    return float(((points - centroids[labels]) ** 2).sum())


def kmeans(points: np.ndarray, k: int, seed: int, iters: int = 100) -> tuple[np.ndarray, np.ndarray, list[float]]:
    points = np.asarray(points, dtype=float)
    if points.ndim != 2 or not 1 <= k <= len(points) or iters < 1:
        raise ValueError("need a 2-D points array, 1 <= k <= n and iters >= 1")
    rng = np.random.default_rng(seed)
    centroids = points[rng.choice(len(points), size=k, replace=False)].copy()
    history = []
    for _ in range(iters):
        labels = assign(points, centroids)
        new = update(points, labels, k, centroids)
        history.append(inertia(points, labels, new))
        converged = np.array_equal(new, centroids)
        centroids = new
        if converged:
            break
    return centroids, assign(points, centroids), history
