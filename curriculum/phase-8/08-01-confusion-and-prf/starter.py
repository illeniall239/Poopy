def confusion_matrix(y_true: list, y_pred: list, labels: list | None = None) -> list[list[int]]:
    """Return M where M[i][j] counts true labels[i] predicted as labels[j]."""
    raise NotImplementedError


def precision_recall_f1(y_true: list, y_pred: list, positive=1) -> tuple[float, float, float]:
    """Return (precision, recall, F1) for the given positive class, with 0/0 defined as 0.0."""
    raise NotImplementedError


def macro_f1(y_true: list, y_pred: list) -> float:
    """Return the unweighted mean of per-class F1 over every label seen."""
    raise NotImplementedError
