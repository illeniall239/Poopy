# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
from collections import Counter


def gini(labels: list) -> float:
    n = len(labels)
    return 1.0 - sum((c / n) ** 2 for c in Counter(labels).values())


def best_split(X: list[list[float]], y: list) -> tuple[int, float, float] | None:
    n = len(y)
    parent = gini(y)
    best, best_gain = None, 1e-12
    for feature in range(len(X[0])):
        values = sorted({row[feature] for row in X})
        for lo, hi in zip(values, values[1:]):
            threshold = (lo + hi) / 2
            left = [label for row, label in zip(X, y) if row[feature] <= threshold]
            right = [label for row, label in zip(X, y) if row[feature] > threshold]
            gain = parent - len(left) / n * gini(left) - len(right) / n * gini(right)
            if gain > best_gain:
                best, best_gain = (feature, threshold, gain), gain
    return best


def majority(y: list):
    counts = Counter(y)
    top = max(counts.values())
    return min(label for label, c in counts.items() if c == top)


def build_tree(X: list[list[float]], y: list, max_depth: int | None = None, min_samples: int = 2) -> dict:
    if not X or len(X) != len(y):
        raise ValueError("X and y must be non-empty and the same length")
    if (max_depth is not None and max_depth < 0) or min_samples < 1:
        raise ValueError("max_depth must be >= 0 (or None) and min_samples >= 1")
    return _grow(X, y, 0, max_depth, min_samples)


def _grow(X, y, depth, max_depth, min_samples) -> dict:
    leaf = {"value": majority(y)}
    if (max_depth is not None and depth >= max_depth) or len(y) < min_samples:
        return leaf
    split = best_split(X, y)  # None for a pure node or when no feature varies
    if split is None:
        return leaf
    feature, threshold, _ = split
    left = [i for i, row in enumerate(X) if row[feature] <= threshold]
    right = [i for i, row in enumerate(X) if row[feature] > threshold]
    return {
        "feature": feature,
        "threshold": threshold,
        "left": _grow([X[i] for i in left], [y[i] for i in left], depth + 1, max_depth, min_samples),
        "right": _grow([X[i] for i in right], [y[i] for i in right], depth + 1, max_depth, min_samples),
    }


def predict_tree(tree: dict, x: list[float]):
    node = tree
    while "value" not in node:
        node = node["left"] if x[node["feature"]] <= node["threshold"] else node["right"]
    return node["value"]
