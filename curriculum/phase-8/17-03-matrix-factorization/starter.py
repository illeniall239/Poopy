import numpy as np


class MatrixFactorization:
    def __init__(self, n_factors: int = 2, lr: float = 0.005, reg: float = 0.01, n_epochs: int = 2000, seed: int = 0):
        """Store the settings; ValueError if n_factors < 1."""
        raise NotImplementedError

    def fit(self, ratings: list[tuple[int, int, float]], n_users: int, n_items: int) -> list[float]:
        """Full-batch gradient descent with L2 on observed cells only; return the loss after each epoch."""
        raise NotImplementedError

    def predict(self, user: int, item: int) -> float:
        """Dot product of the user's and item's learned vectors."""
        raise NotImplementedError

    def rmse(self, ratings: list[tuple[int, int, float]]) -> float:
        """Root mean squared error of predict over the given (user, item, rating) triples."""
        raise NotImplementedError
