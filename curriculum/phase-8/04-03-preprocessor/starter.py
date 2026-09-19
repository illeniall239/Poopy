import numpy as np


class Preprocessor:
    def __init__(self, spec: dict[str, dict]):
        """Validate the column spec: kinds numeric, log, bucket (with boundaries) and category."""
        raise NotImplementedError

    def fit(self, rows: list[dict]) -> "Preprocessor":
        """Learn means, stds and sorted vocabularies from the training rows only; return self."""
        raise NotImplementedError

    def transform(self, rows: list[dict]) -> np.ndarray:
        """Encode rows with the stored statistics into a (len(rows), n_features) float array."""
        raise NotImplementedError
