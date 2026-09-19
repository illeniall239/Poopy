# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
def mean_baseline(train_ys: list[float]) -> float:
    if not train_ys:
        raise ValueError("no training targets")
    return sum(train_ys) / len(train_ys)


def mse(y_true: list[float], y_pred: list[float]) -> float:
    if not y_true or len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must be non-empty and the same length")
    return sum((t - p) ** 2 for t, p in zip(y_true, y_pred)) / len(y_true)


def baseline_mse(train_ys: list[float], val_ys: list[float]) -> float:
    prediction = mean_baseline(train_ys)
    return mse(val_ys, [prediction] * len(val_ys))
