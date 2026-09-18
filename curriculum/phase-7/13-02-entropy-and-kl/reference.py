# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import math


def _check(p: list[float]) -> None:
    if not p or any(x < 0 for x in p) or abs(sum(p) - 1.0) > 1e-9:
        raise ValueError("not a probability distribution")


def entropy(p: list[float]) -> float:
    _check(p)
    return -sum(x * math.log(x) for x in p if x > 0)


def cross_entropy(p: list[float], q: list[float]) -> float:
    _check(p)
    _check(q)
    if len(p) != len(q):
        raise ValueError("length mismatch")
    total = 0.0
    for pi, qi in zip(p, q):
        if pi == 0:
            continue
        if qi == 0:
            return math.inf
        total -= pi * math.log(qi)
    return total


def kl(p: list[float], q: list[float]) -> float:
    return cross_entropy(p, q) - entropy(p)
