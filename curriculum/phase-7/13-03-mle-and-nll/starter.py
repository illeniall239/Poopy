def mle_bernoulli(ys: list[int]) -> float:
    """Fraction of ones; ValueError on empty input or values outside {0, 1}."""
    raise NotImplementedError


def mle_gaussian(xs: list[float]) -> tuple[float, float]:
    """(mean, variance with ddof=0); ValueError on empty input."""
    raise NotImplementedError


def nll_bernoulli(ys: list[int], ps: list[float]) -> float:
    """Mean binary cross-entropy with ps clipped to [1e-12, 1 - 1e-12]; ValueError on invalid input."""
    raise NotImplementedError
