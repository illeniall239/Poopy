# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
def _check(y_true: list, y_pred: list) -> None:
    if not y_true or len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must be non-empty and the same length")


def _safe_div(a: float, b: float) -> float:
    return a / b if b else 0.0


def confusion_matrix(y_true: list, y_pred: list, labels: list | None = None) -> list[list[int]]:
    _check(y_true, y_pred)
    if labels is None:
        labels = sorted(set(y_true) | set(y_pred))
    index = {label: i for i, label in enumerate(labels)}
    matrix = [[0] * len(labels) for _ in labels]
    for t, p in zip(y_true, y_pred):
        if t not in index or p not in index:
            raise ValueError(f"label not in labels: {t if t not in index else p!r}")
        matrix[index[t]][index[p]] += 1
    return matrix


def precision_recall_f1(y_true: list, y_pred: list, positive=1) -> tuple[float, float, float]:
    _check(y_true, y_pred)
    tp = sum(1 for t, p in zip(y_true, y_pred) if t == positive and p == positive)
    fp = sum(1 for t, p in zip(y_true, y_pred) if t != positive and p == positive)
    fn = sum(1 for t, p in zip(y_true, y_pred) if t == positive and p != positive)
    precision = _safe_div(tp, tp + fp)
    recall = _safe_div(tp, tp + fn)
    f1 = _safe_div(2 * precision * recall, precision + recall)
    return precision, recall, f1


def macro_f1(y_true: list, y_pred: list) -> float:
    _check(y_true, y_pred)
    labels = sorted(set(y_true) | set(y_pred))
    return sum(precision_recall_f1(y_true, y_pred, label)[2] for label in labels) / len(labels)
