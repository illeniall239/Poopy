def pearson(x: list[float], y: list[float]) -> float:
    """Pearson correlation coefficient; ValueError on length mismatch, n < 2 or a constant input."""
    raise NotImplementedError


def rank(values: list[float]) -> list[float]:
    """1-based ranks with ties given the average rank."""
    raise NotImplementedError


def spearman(x: list[float], y: list[float]) -> float:
    """Pearson correlation of the average ranks of x and y."""
    raise NotImplementedError
