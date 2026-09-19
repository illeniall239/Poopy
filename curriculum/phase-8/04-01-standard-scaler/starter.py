import numpy as np


class StandardScaler:
    def fit(self, train: np.ndarray) -> "StandardScaler":
        """Store per-column mean_ and scale_ (population std, 1.0 for constant columns); return self."""
        raise NotImplementedError

    def transform(self, rows: np.ndarray) -> np.ndarray:
        """Return (rows - mean_) / scale_ using the fitted statistics only."""
        raise NotImplementedError
