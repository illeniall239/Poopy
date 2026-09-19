import numpy as np


def kmeans_pp_init(points: np.ndarray, k: int, rng: np.random.Generator) -> np.ndarray:
    """k starting centroids chosen by k-means++ (each new one drawn with probability proportional to D^2)."""
    raise NotImplementedError


def inertia_curve(points: np.ndarray, ks: list[int], seed: int) -> list[float]:
    """Final Lloyd inertia for each k in ks, starting from k-means++ with a fresh default_rng(seed) per k."""
    raise NotImplementedError
