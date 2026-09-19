import numpy as np


def kmeans(points: np.ndarray, k: int, seed: int, iters: int = 100) -> tuple[np.ndarray, np.ndarray, list[float]]:
    """Lloyd's algorithm from k seeded random points; return (centroids, labels, inertia history)."""
    raise NotImplementedError
