# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import math
from collections import Counter


def _proportions(labels: list) -> list[float]:
    if not labels:
        raise ValueError("labels must not be empty")
    n = len(labels)
    return [count / n for count in Counter(labels).values()]


def gini(labels: list) -> float:
    return 1.0 - sum(p * p for p in _proportions(labels))


def entropy(labels: list) -> float:
    # Every p here is > 0: Counter only holds classes that occur.
    # Adding 0.0 turns the -0.0 of a pure node into a plain 0.0.
    return -sum(p * math.log2(p) for p in _proportions(labels)) + 0.0
