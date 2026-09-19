# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import numpy as np


class StandardScaler:
    def fit(self, train: np.ndarray) -> "StandardScaler":
        train = np.asarray(train, dtype=float)
        if train.ndim != 2 or train.shape[0] == 0:
            raise ValueError("train must be a 2-D array with at least one row")
        self.mean_ = train.mean(axis=0)
        std = train.std(axis=0)
        self.scale_ = np.where(std == 0, 1.0, std)
        return self

    def transform(self, rows: np.ndarray) -> np.ndarray:
        if not hasattr(self, "mean_"):
            raise RuntimeError("call fit before transform")
        rows = np.asarray(rows, dtype=float)
        if rows.ndim != 2 or rows.shape[1] != self.mean_.shape[0]:
            raise ValueError(f"rows must be 2-D with {self.mean_.shape[0]} columns")
        return (rows - self.mean_) / self.scale_
