def mean_ci(sample: list[float], z: float = 1.96) -> tuple[float, float]:
    """Normal-approximation interval for the mean, mean ± z * s / sqrt(n) with ddof=1; ValueError if n < 2."""
    raise NotImplementedError


def proportion_ci(successes: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """p ± z * sqrt(p(1-p)/n) clipped to [0, 1]; ValueError on invalid counts."""
    raise NotImplementedError


def sample_size_for_margin(margin: float, z: float = 1.96, p: float = 0.5) -> int:
    """Smallest n with z * sqrt(p(1-p)/n) <= margin; ValueError on invalid margin or p."""
    raise NotImplementedError
