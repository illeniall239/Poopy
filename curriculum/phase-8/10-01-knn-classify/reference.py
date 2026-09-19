# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import numpy as np


def knn_predict(train_X: np.ndarray, train_y: np.ndarray, x: np.ndarray, k: int) -> int:
    train_X = np.asarray(train_X, dtype=float)
    train_y = np.asarray(train_y)
    x = np.asarray(x, dtype=float)
    if train_X.ndim != 2 or train_y.shape != (train_X.shape[0],) or x.shape != (train_X.shape[1],):
        raise ValueError("need train_X (n, d), train_y (n,) and x (d,)")
    if not 1 <= k <= len(train_X):
        raise ValueError("k must be between 1 and n")
    distances = np.linalg.norm(train_X - x, axis=1)
    nearest = np.argsort(distances, kind="stable")[:k]  # equal distances keep index order

    votes: dict[int, int] = {}
    closest: dict[int, float] = {}
    for i in nearest:  # walked nearest-first, so the first sighting of a label is its closest member
        label = int(train_y[i])
        votes[label] = votes.get(label, 0) + 1
        closest.setdefault(label, float(distances[i]))

    top = max(votes.values())
    tied = [label for label, count in votes.items() if count == top]
    return min(tied, key=lambda label: (closest[label], label))
