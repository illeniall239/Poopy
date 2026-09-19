# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import numpy as np


class Pipeline:
    def __init__(self, steps: list, model):
        self.steps = steps
        self.model = model

    def _transform(self, X: np.ndarray) -> np.ndarray:
        for step in self.steps:
            X = step.transform(X)
        return X

    def fit(self, X: np.ndarray, y: np.ndarray) -> "Pipeline":
        for step in self.steps:
            step.fit(X)
            X = step.transform(X)
        self.model.fit(X, y)
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict(self._transform(X))


def cross_val_score(pipeline: Pipeline, X: np.ndarray, y: np.ndarray, folds: list, metric) -> list[float]:
    if not folds:
        raise ValueError("need at least one fold")
    X, y = np.asarray(X), np.asarray(y)
    scores = []
    for train_idx, val_idx in folds:
        train_idx, val_idx = np.asarray(train_idx), np.asarray(val_idx)
        pipeline.fit(X[train_idx], y[train_idx])  # every step is refitted on this fold's training rows only
        scores.append(float(metric(y[val_idx], pipeline.predict(X[val_idx]))))
    return scores
