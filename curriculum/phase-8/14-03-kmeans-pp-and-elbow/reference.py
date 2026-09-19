# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import numpy as np


def squared_distances(points: np.ndarray, centroids: np.ndarray) -> np.ndarray:
    return ((points[:, None, :] - centroids[None, :, :]) ** 2).sum(axis=2)


def kmeans_pp_init(points: np.ndarray, k: int, rng: np.random.Generator) -> np.ndarray:
    points = np.asarray(points, dtype=float)
    n = len(points)
    if points.ndim != 2 or not 1 <= k <= n:
        raise ValueError("need a 2-D points array and 1 <= k <= n")
    chosen = [int(rng.integers(n))]
    for _ in range(k - 1):
        d2 = squared_distances(points, points[chosen]).min(axis=1)
        total = d2.sum()
        if total == 0:
            raise ValueError("fewer distinct points than k")
        chosen.append(int(rng.choice(n, p=d2 / total)))  # far points are proportionally more likely
    return points[chosen].copy()


def lloyd(points: np.ndarray, centroids: np.ndarray, iters: int = 100) -> tuple[np.ndarray, float]:
    k = len(centroids)
    for _ in range(iters):
        labels = squared_distances(points, centroids).argmin(axis=1)
        new = centroids.copy()
        for c in range(k):
            members = points[labels == c]
            if len(members):
                new[c] = members.mean(axis=0)
        converged = np.array_equal(new, centroids)
        centroids = new
        if converged:
            break
    return centroids, float(squared_distances(points, centroids).min(axis=1).sum())


def inertia_curve(points: np.ndarray, ks: list[int], seed: int) -> list[float]:
    points = np.asarray(points, dtype=float)
    curve = []
    for k in ks:
        start = kmeans_pp_init(points, k, np.random.default_rng(seed))  # a fresh generator per k
        _, inertia = lloyd(points, start)
        curve.append(inertia)
    return curve
