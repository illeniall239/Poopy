# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import numpy as np


class MatrixFactorization:
    def __init__(self, n_factors: int = 2, lr: float = 0.005, reg: float = 0.01, n_epochs: int = 2000, seed: int = 0):
        if n_factors < 1:
            raise ValueError("n_factors must be at least 1")
        self.n_factors, self.lr, self.reg, self.n_epochs, self.seed = n_factors, lr, reg, n_epochs, seed
        self.P = None
        self.Q = None

    def fit(self, ratings: list[tuple[int, int, float]], n_users: int, n_items: int) -> list[float]:
        if not ratings:
            raise ValueError("no ratings")
        users = np.array([u for u, _, _ in ratings])
        items = np.array([i for _, i, _ in ratings])
        values = np.array([r for _, _, r in ratings], dtype=float)
        if users.min() < 0 or users.max() >= n_users or items.min() < 0 or items.max() >= n_items:
            raise ValueError("a rating refers to a user or item out of range")

        # Dense views of the observed cells; the mask keeps unobserved cells out of the loss.
        R = np.zeros((n_users, n_items))
        mask = np.zeros((n_users, n_items))
        R[users, items] = values
        mask[users, items] = 1.0

        rng = np.random.default_rng(self.seed)
        P = rng.normal(0.0, 0.1, size=(n_users, self.n_factors))
        Q = rng.normal(0.0, 0.1, size=(n_items, self.n_factors))

        losses = []
        for _ in range(self.n_epochs):
            E = mask * (P @ Q.T - R)  # residuals on observed cells, 0 elsewhere
            grad_P = 2 * E @ Q + 2 * self.reg * P
            grad_Q = 2 * E.T @ P + 2 * self.reg * Q
            P, Q = P - self.lr * grad_P, Q - self.lr * grad_Q
            E = mask * (P @ Q.T - R)
            losses.append(float(np.sum(E**2) + self.reg * (np.sum(P**2) + np.sum(Q**2))))
        self.P, self.Q = P, Q
        return losses

    def predict(self, user: int, item: int) -> float:
        if self.P is None:
            raise RuntimeError("call fit first")
        return float(self.P[user] @ self.Q[item])

    def rmse(self, ratings: list[tuple[int, int, float]]) -> float:
        errors = [(self.predict(u, i) - r) ** 2 for u, i, r in ratings]
        return float(np.sqrt(np.mean(errors)))
