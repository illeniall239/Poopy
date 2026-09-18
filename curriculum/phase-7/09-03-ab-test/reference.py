# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import math
import random


def two_proportion_ztest(successes_a: int, n_a: int, successes_b: int, n_b: int) -> tuple[float, float]:
    if n_a <= 0 or n_b <= 0 or not 0 <= successes_a <= n_a or not 0 <= successes_b <= n_b:
        raise ValueError("invalid counts")
    p_a, p_b = successes_a / n_a, successes_b / n_b
    pooled = (successes_a + successes_b) / (n_a + n_b)
    if pooled in (0.0, 1.0):
        return 0.0, 1.0
    se = math.sqrt(pooled * (1 - pooled) * (1 / n_a + 1 / n_b))
    z = (p_b - p_a) / se
    return z, math.erfc(abs(z) / math.sqrt(2))


def _mean(xs: list[float]) -> float:
    return sum(xs) / len(xs)


def permutation_test(a: list[float], b: list[float], n_permutations: int, rng: random.Random) -> float:
    observed = abs(_mean(b) - _mean(a))
    pool = list(a) + list(b)
    n_a = len(a)
    count = 0
    for _ in range(n_permutations):
        rng.shuffle(pool)
        if abs(_mean(pool[n_a:]) - _mean(pool[:n_a])) >= observed:
            count += 1
    return (count + 1) / (n_permutations + 1)


def bootstrap_diff_ci(
    a: list[float], b: list[float], n_bootstrap: int, rng: random.Random, alpha: float = 0.05
) -> tuple[float, float]:
    diffs = sorted(
        _mean(rng.choices(b, k=len(b))) - _mean(rng.choices(a, k=len(a))) for _ in range(n_bootstrap)
    )
    lo = diffs[math.floor(alpha / 2 * (n_bootstrap - 1))]
    hi = diffs[math.floor((1 - alpha / 2) * (n_bootstrap - 1))]
    return lo, hi
