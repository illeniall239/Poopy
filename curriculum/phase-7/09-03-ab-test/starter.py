import random


def two_proportion_ztest(successes_a: int, n_a: int, successes_b: int, n_b: int) -> tuple[float, float]:
    """(z, two-sided p) for the pooled two-proportion z-test via math.erfc; ValueError on invalid counts."""
    raise NotImplementedError


def permutation_test(a: list[float], b: list[float], n_permutations: int, rng: random.Random) -> float:
    """Two-sided permutation p-value (count + 1) / (n + 1) for the difference in means mean(b) - mean(a)."""
    raise NotImplementedError


def bootstrap_diff_ci(
    a: list[float], b: list[float], n_bootstrap: int, rng: random.Random, alpha: float = 0.05
) -> tuple[float, float]:
    """Percentile bootstrap interval for mean(b) - mean(a) at level 1 - alpha."""
    raise NotImplementedError
