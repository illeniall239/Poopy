def slice_metrics(y_true: list, y_pred: list, feature_values: list, metric) -> list[tuple]:
    """(value, score, support) per feature-value slice, worst score first, ties by first appearance."""
    raise NotImplementedError


def worst_errors(y_true: list[int], scores: list[float], n: int) -> list[int]:
    """Indices of up to n misclassified rows, most confident (|score - 0.5|) first, ties by index."""
    raise NotImplementedError
