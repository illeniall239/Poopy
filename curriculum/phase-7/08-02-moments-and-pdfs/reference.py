# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import math


def mean(sample: list[float]) -> float:
    if not sample:
        raise ValueError("empty sample")
    return sum(sample) / len(sample)


def variance(sample: list[float], ddof: int = 0) -> float:
    n = len(sample)
    if n - ddof <= 0:
        raise ValueError("need more than ddof values")
    m = mean(sample)
    return sum((x - m) ** 2 for x in sample) / (n - ddof)


def expectation(values: list[float], probs: list[float]) -> float:
    if len(values) != len(probs):
        raise ValueError("length mismatch")
    if any(p < 0 for p in probs) or abs(sum(probs) - 1.0) > 1e-9:
        raise ValueError("probs must be non-negative and sum to 1")
    return sum(v * p for v, p in zip(values, probs))


def gaussian_pdf(x: float, mu: float = 0.0, sigma: float = 1.0) -> float:
    if sigma <= 0:
        raise ValueError("sigma must be positive")
    z = (x - mu) / sigma
    return math.exp(-0.5 * z * z) / (sigma * math.sqrt(2 * math.pi))


def bernoulli_pmf(k: int, p: float) -> float:
    if not 0.0 <= p <= 1.0:
        raise ValueError("p must lie in [0, 1]")
    if k == 1:
        return p
    if k == 0:
        return 1.0 - p
    return 0.0
