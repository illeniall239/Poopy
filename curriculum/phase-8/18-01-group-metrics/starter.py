def group_metrics(y_true: list[int], y_pred: list[int], groups: list) -> dict:
    """Per group: n, selection_rate, tpr (None if no positives), fpr (None if no negatives), accuracy."""
    raise NotImplementedError
