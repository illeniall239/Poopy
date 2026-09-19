def pr_curve(y_true: list[int], scores: list[float]) -> list[tuple[float, float, float]]:
    """Return (threshold, precision, recall) for each distinct score, highest threshold first."""
    raise NotImplementedError


def best_threshold(
    y_true: list[int], scores: list[float], metric: str = "f1", min_precision: float | None = None
) -> float:
    """Return the threshold maximizing F1, or recall subject to precision >= min_precision; ties go to the higher threshold."""
    raise NotImplementedError
