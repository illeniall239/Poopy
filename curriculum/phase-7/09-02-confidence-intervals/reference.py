# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
import math


def mean_ci(sample: list[float], z: float = 1.96) -> tuple[float, float]:
    n = len(sample)
    if n < 2:
        raise ValueError("need at least two values")
    m = sum(sample) / n
    s = math.sqrt(sum((x - m) ** 2 for x in sample) / (n - 1))
    half = z * s / math.sqrt(n)
    return m - half, m + half


def proportion_ci(successes: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n <= 0 or not 0 <= successes <= n:
        raise ValueError("need 0 <= successes <= n and n > 0")
    p = successes / n
    half = z * math.sqrt(p * (1 - p) / n)
    return max(0.0, p - half), min(1.0, p + half)


def sample_size_for_margin(margin: float, z: float = 1.96, p: float = 0.5) -> int:
    if margin <= 0 or not 0 <= p <= 1:
        raise ValueError("margin must be positive and p in [0, 1]")
    return math.ceil(z * z * p * (1 - p) / (margin * margin))
