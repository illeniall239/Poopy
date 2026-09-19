# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import numpy as np


class GaussianAnomalyDetector:
    def __init__(self):
        self.mean_ = None
        self.var_ = None

    def fit(self, X: np.ndarray) -> "GaussianAnomalyDetector":
        X = np.asarray(X, dtype=float)
        if X.ndim != 2 or X.shape[0] == 0:
            raise ValueError("X must be a non-empty 2-D array")
        var = X.var(axis=0)
        if np.any(var == 0):
            raise ValueError("a column has zero variance")
        self.mean_, self.var_ = X.mean(axis=0), var
        return self

    def score(self, X: np.ndarray) -> np.ndarray:
        if self.mean_ is None:
            raise RuntimeError("call fit first")
        X = np.asarray(X, dtype=float)
        per_feature = -0.5 * np.log(2 * np.pi * self.var_) - (X - self.mean_) ** 2 / (2 * self.var_)
        return per_feature.sum(axis=1)

    @staticmethod
    def choose_epsilon(scores: np.ndarray, labels: np.ndarray) -> tuple[float, float]:
        scores = np.asarray(scores, dtype=float)
        labels = np.asarray(labels).astype(bool)
        if scores.shape != labels.shape:
            raise ValueError("scores and labels must have the same length")
        if not labels.any():
            raise ValueError("need at least one labeled anomaly")
        best_eps, best_f1 = None, -1.0
        for eps in np.unique(scores):  # ascending, so a strict > keeps the smallest on ties
            flagged = scores <= eps
            tp = np.sum(flagged & labels)
            fp = np.sum(flagged & ~labels)
            fn = np.sum(~flagged & labels)
            f1 = 2 * tp / (2 * tp + fp + fn) if tp else 0.0
            if f1 > best_f1:
                best_eps, best_f1 = float(eps), float(f1)
        return best_eps, best_f1
