# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import math


def zscore_flags(xs: list[float], k: float = 3.0) -> list[bool]:
    if not xs:
        raise ValueError("no values")
    mean = sum(xs) / len(xs)
    std = math.sqrt(sum((x - mean) ** 2 for x in xs) / len(xs))
    if std == 0:
        return [False] * len(xs)
    return [abs(x - mean) / std > k for x in xs]


def _quantile(sorted_xs: list[float], p: float) -> float:
    pos = p * (len(sorted_xs) - 1)
    lo = math.floor(pos)
    hi = min(lo + 1, len(sorted_xs) - 1)
    return sorted_xs[lo] + (pos - lo) * (sorted_xs[hi] - sorted_xs[lo])


def iqr_flags(xs: list[float], factor: float = 1.5) -> list[bool]:
    if not xs:
        raise ValueError("no values")
    s = sorted(xs)
    q1, q3 = _quantile(s, 0.25), _quantile(s, 0.75)
    low, high = q1 - factor * (q3 - q1), q3 + factor * (q3 - q1)
    return [x < low or x > high for x in xs]
