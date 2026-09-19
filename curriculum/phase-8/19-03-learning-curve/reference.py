# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import numpy as np


def _mse(y_true: np.ndarray, y_pred) -> float:
    return float(np.mean((np.asarray(y_true, dtype=float) - np.asarray(y_pred, dtype=float)) ** 2))


def learning_curve(fit, predict, X: np.ndarray, y: np.ndarray, sizes: list[int], folds: list) -> list[tuple[int, float, float]]:
    if not sizes or not folds:
        raise ValueError("need at least one size and one fold")
    shortest = min(len(train_idx) for train_idx, _ in folds)
    if any(s < 1 or s > shortest for s in sizes):
        raise ValueError("every size must be between 1 and the smallest training fold")

    X, y = np.asarray(X), np.asarray(y)
    curve = []
    for s in sizes:
        train_errors, val_errors = [], []
        for train_idx, val_idx in folds:
            subset = np.asarray(train_idx[:s])
            val = np.asarray(val_idx)
            model = fit(X[subset], y[subset])
            train_errors.append(_mse(y[subset], predict(model, X[subset])))
            val_errors.append(_mse(y[val], predict(model, X[val])))
        curve.append((s, float(np.mean(train_errors)), float(np.mean(val_errors))))
    return curve


def more_data_helps(curve: list[tuple[int, float, float]], tol: float = 1e-3) -> bool:
    if len(curve) < 2:
        raise ValueError("need at least two points on the curve")
    gaps = [val - train for _, train, val in curve]
    still_open = gaps[-1] > tol
    still_closing = gaps[-2] - gaps[-1] > tol
    return still_open and still_closing
