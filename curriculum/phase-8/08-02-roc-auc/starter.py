def roc_auc(y_true: list[int], scores: list[float]) -> float:
    """Return ROC AUC via average ranks (Mann–Whitney), ties counting one half."""
    raise NotImplementedError


def roc_curve(y_true: list[int], scores: list[float]) -> tuple[list[float], list[float]]:
    """Return (fpr, tpr) from (0, 0) through one point per distinct score, descending, to (1, 1)."""
    raise NotImplementedError


def auc_trapezoid(fpr: list[float], tpr: list[float]) -> float:
    """Return the area under the polyline through (fpr, tpr) by the trapezoid rule."""
    raise NotImplementedError
