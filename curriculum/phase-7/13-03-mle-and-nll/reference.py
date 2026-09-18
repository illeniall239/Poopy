# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
import math

EPS = 1e-12


def mle_bernoulli(ys: list[int]) -> float:
    if not ys or any(y not in (0, 1) for y in ys):
        raise ValueError("ys must be a non-empty list of 0/1 values")
    return sum(ys) / len(ys)


def mle_gaussian(xs: list[float]) -> tuple[float, float]:
    if not xs:
        raise ValueError("empty sample")
    m = sum(xs) / len(xs)
    return m, sum((x - m) ** 2 for x in xs) / len(xs)


def nll_bernoulli(ys: list[int], ps: list[float]) -> float:
    if not ys or len(ys) != len(ps):
        raise ValueError("ys and ps must be non-empty and the same length")
    if any(y not in (0, 1) for y in ys) or any(not 0.0 <= p <= 1.0 for p in ps):
        raise ValueError("ys must be 0/1 and ps in [0, 1]")
    total = 0.0
    for y, p in zip(ys, ps):
        p = min(max(p, EPS), 1 - EPS)
        total -= y * math.log(p) + (1 - y) * math.log(1 - p)
    return total / len(ys)
