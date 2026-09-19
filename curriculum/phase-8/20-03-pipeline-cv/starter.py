import numpy as np


class Pipeline:
    def __init__(self, steps: list, model):
        """Store the preprocessing steps (in order) and the final model."""
        raise NotImplementedError

    def fit(self, X: np.ndarray, y: np.ndarray) -> "Pipeline":
        """Fit and apply each step in order, then fit the model on the result; return self."""
        raise NotImplementedError

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Transform X through every step (no refitting), then predict with the model."""
        raise NotImplementedError


def cross_val_score(pipeline: Pipeline, X: np.ndarray, y: np.ndarray, folds: list, metric) -> list[float]:
    """Per-fold metric(y_val, predictions) with the whole pipeline refitted on each fold's training rows."""
    raise NotImplementedError
