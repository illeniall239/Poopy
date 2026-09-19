import numpy as np


class GaussianAnomalyDetector:
    def fit(self, X: np.ndarray) -> "GaussianAnomalyDetector":
        """Store per-column mean and population variance of normal rows; return self."""
        raise NotImplementedError

    def score(self, X: np.ndarray) -> np.ndarray:
        """Per-row log density under independent per-feature Gaussians (lower = more anomalous)."""
        raise NotImplementedError

    @staticmethod
    def choose_epsilon(scores: np.ndarray, labels: np.ndarray) -> tuple[float, float]:
        """(epsilon, F1) of the threshold flagging score <= epsilon that maximizes F1; smallest on ties."""
        raise NotImplementedError
