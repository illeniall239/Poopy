# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import numpy as np


def _fold_bounds(n: int, folds: int) -> list[tuple[int, int]]:
    """(start, stop) of each contiguous validation block; the first n % folds blocks get one extra row."""
    q, r = divmod(n, folds)
    bounds, start = [], 0
    for f in range(folds):
        stop = start + q + (1 if f < r else 0)
        bounds.append((start, stop))
        start = stop
    return bounds


def _vote(labels: np.ndarray, distances: np.ndarray) -> int:
    """Majority label; ties by nearest member, then smallest label. Inputs are sorted nearest-first."""
    votes: dict[int, int] = {}
    closest: dict[int, float] = {}
    for label, dist in zip(labels.tolist(), distances.tolist()):
        votes[label] = votes.get(label, 0) + 1
        closest.setdefault(label, dist)
    top = max(votes.values())
    return min((label for label, c in votes.items() if c == top), key=lambda label: (closest[label], label))


def _fold_accuracies(X: np.ndarray, y: np.ndarray, ks: list[int], folds: int) -> dict[int, float]:
    n = len(X)
    if not 2 <= folds <= n:
        raise ValueError("folds must be between 2 and n")
    if not ks:
        raise ValueError("ks must not be empty")
    bounds = _fold_bounds(n, folds)
    smallest_train = n - max(stop - start for start, stop in bounds)
    if any(not 1 <= k <= smallest_train for k in ks):
        raise ValueError(f"every k must be between 1 and {smallest_train}")

    totals = {k: 0.0 for k in ks}
    for start, stop in bounds:
        train = np.r_[0:start, stop:n]  # original order, so position order == index order
        dist = np.linalg.norm(X[start:stop, None, :] - X[None, train, :], axis=2)
        order = np.argsort(dist, axis=1, kind="stable")  # shared by every k
        for k in totals:
            correct = 0
            for row in range(stop - start):
                nearest = order[row, :k]
                correct += _vote(y[train][nearest], dist[row, nearest]) == y[start + row]
            totals[k] += correct / (stop - start)
    return {k: total / folds for k, total in totals.items()}


def cv_accuracy(X: np.ndarray, y: np.ndarray, k: int, folds: int) -> float:
    return _fold_accuracies(np.asarray(X, dtype=float), np.asarray(y), [k], folds)[k]


def choose_k(X: np.ndarray, y: np.ndarray, ks: list[int], folds: int) -> int:
    scores = _fold_accuracies(np.asarray(X, dtype=float), np.asarray(y), list(ks), folds)
    return min(scores, key=lambda k: (-scores[k], k))
