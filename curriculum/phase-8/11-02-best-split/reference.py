# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
from collections import Counter


def gini(labels: list) -> float:
    n = len(labels)
    return 1.0 - sum((c / n) ** 2 for c in Counter(labels).values())


def best_split(X: list[list[float]], y: list) -> tuple[int, float, float] | None:
    if not X or len(X) != len(y):
        raise ValueError("X and y must be non-empty and the same length")
    n = len(y)
    parent = gini(y)
    best = None
    best_gain = 1e-12  # a split must beat this to count, so a zero-gain split is never returned
    for feature in range(len(X[0])):
        values = sorted({row[feature] for row in X})
        for lo, hi in zip(values, values[1:]):
            threshold = (lo + hi) / 2
            left = [label for row, label in zip(X, y) if row[feature] <= threshold]
            right = [label for row, label in zip(X, y) if row[feature] > threshold]
            children = len(left) / n * gini(left) + len(right) / n * gini(right)
            gain = parent - children
            if gain > best_gain:  # strict: ties keep the earlier feature and smaller threshold
                best, best_gain = (feature, threshold, gain), gain
    return best
