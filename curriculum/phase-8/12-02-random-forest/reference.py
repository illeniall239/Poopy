# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import math
import random
from collections import Counter


def gini(labels: list) -> float:
    n = len(labels)
    return 1.0 - sum((c / n) ** 2 for c in Counter(labels).values())


def majority(labels: list):
    counts = Counter(labels)
    top = max(counts.values())
    return min(label for label, c in counts.items() if c == top)


def best_split(X: list[list[float]], y: list, features: list[int]) -> tuple[int, float] | None:
    n = len(y)
    parent = gini(y)
    best, best_gain = None, 1e-12
    for feature in sorted(features):
        values = sorted({row[feature] for row in X})
        for lo, hi in zip(values, values[1:]):
            threshold = (lo + hi) / 2
            left = [label for row, label in zip(X, y) if row[feature] <= threshold]
            right = [label for row, label in zip(X, y) if row[feature] > threshold]
            gain = parent - len(left) / n * gini(left) - len(right) / n * gini(right)
            if gain > best_gain:
                best, best_gain = (feature, threshold), gain
    return best


def predict_tree(tree: dict, x: list[float]):
    node = tree
    while "value" not in node:
        node = node["left"] if x[node["feature"]] <= node["threshold"] else node["right"]
    return node["value"]


class RandomForest:
    def __init__(
        self,
        n_trees: int = 25,
        max_features: int | None = None,
        max_depth: int | None = None,
        min_samples: int = 2,
        seed: int = 0,
    ):
        self.n_trees = n_trees
        self.max_features = max_features
        self.max_depth = max_depth
        self.min_samples = min_samples
        self.seed = seed
        self.trees: list[dict] = []

    def fit(self, X: list[list[float]], y: list) -> "RandomForest":
        if not X or len(X) != len(y):
            raise ValueError("X and y must be non-empty and the same length")
        d = len(X[0])
        m = self.max_features if self.max_features is not None else max(1, int(math.sqrt(d)))
        if self.n_trees < 1 or not 1 <= m <= d:
            raise ValueError("need n_trees >= 1 and 1 <= max_features <= number of features")
        self._m = m
        self._d = d
        self._rng = random.Random(self.seed)
        n = len(y)
        self.trees = []
        for _ in range(self.n_trees):
            rows = [self._rng.randrange(n) for _ in range(n)]  # bootstrap: with replacement
            self.trees.append(self._grow([X[i] for i in rows], [y[i] for i in rows], 0))
        return self

    def _grow(self, X: list[list[float]], y: list, depth: int) -> dict:
        leaf = {"value": majority(y)}
        if (self.max_depth is not None and depth >= self.max_depth) or len(y) < self.min_samples:
            return leaf
        features = self._rng.sample(range(self._d), self._m)  # a fresh random subset at every split
        split = best_split(X, y, features)
        if split is None:
            return leaf
        feature, threshold = split
        left = [i for i, row in enumerate(X) if row[feature] <= threshold]
        right = [i for i, row in enumerate(X) if row[feature] > threshold]
        return {
            "feature": feature,
            "threshold": threshold,
            "left": self._grow([X[i] for i in left], [y[i] for i in left], depth + 1),
            "right": self._grow([X[i] for i in right], [y[i] for i in right], depth + 1),
        }

    def predict(self, X: list[list[float]]) -> list:
        if not self.trees:
            raise RuntimeError("call fit before predict")
        return [majority([predict_tree(tree, x) for tree in self.trees]) for x in X]
