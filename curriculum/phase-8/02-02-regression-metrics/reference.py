# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import math


def _check(y_true: list[float], y_pred: list[float]) -> None:
    if not y_true or len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must be non-empty and the same length")


def mse(y_true: list[float], y_pred: list[float]) -> float:
    _check(y_true, y_pred)
    return sum((t - p) ** 2 for t, p in zip(y_true, y_pred)) / len(y_true)


def mae(y_true: list[float], y_pred: list[float]) -> float:
    _check(y_true, y_pred)
    return sum(abs(t - p) for t, p in zip(y_true, y_pred)) / len(y_true)


def rmse(y_true: list[float], y_pred: list[float]) -> float:
    return math.sqrt(mse(y_true, y_pred))


def r2(y_true: list[float], y_pred: list[float]) -> float:
    _check(y_true, y_pred)
    if all(t == y_true[0] for t in y_true):
        raise ValueError("y_true is constant; R² is undefined")
    mean = sum(y_true) / len(y_true)
    ss_res = sum((t - p) ** 2 for t, p in zip(y_true, y_pred))
    ss_tot = sum((t - mean) ** 2 for t in y_true)
    return 1.0 - ss_res / ss_tot
