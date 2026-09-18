def mean(sample: list[float]) -> float:
    """Arithmetic mean; ValueError on an empty sample."""
    raise NotImplementedError


def variance(sample: list[float], ddof: int = 0) -> float:
    """Mean squared deviation divided by n - ddof; ValueError if n - ddof <= 0."""
    raise NotImplementedError


def expectation(values: list[float], probs: list[float]) -> float:
    """Sum of value * probability; ValueError on length mismatch or invalid probabilities."""
    raise NotImplementedError


def gaussian_pdf(x: float, mu: float = 0.0, sigma: float = 1.0) -> float:
    """Normal density at x; ValueError if sigma <= 0."""
    raise NotImplementedError


def bernoulli_pmf(k: int, p: float) -> float:
    """p for k=1, 1-p for k=0, 0 otherwise; ValueError if p is outside [0, 1]."""
    raise NotImplementedError
