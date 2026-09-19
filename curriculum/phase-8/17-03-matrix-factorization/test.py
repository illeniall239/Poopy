import time
import unittest

import numpy as np

from solution import MatrixFactorization


def planted(seed, n_users=30, n_items=40, held_out=0.2):
    """A rank-2 ratings matrix in roughly [0.5, 4.5], split into observed and held-out cells."""
    rng = np.random.default_rng(seed)
    U = rng.uniform(0.5, 1.5, size=(n_users, 2))
    V = rng.uniform(0.5, 1.5, size=(n_items, 2))
    R = U @ V.T
    cells = [(u, i, float(R[u, i])) for u in range(n_users) for i in range(n_items)]
    order = rng.permutation(len(cells))
    cut = int(len(cells) * (1 - held_out))
    train = [cells[j] for j in order[:cut]]
    test = [cells[j] for j in order[cut:]]
    return train, test


class TestMatrixFactorization(unittest.TestCase):
    def test_held_out_rmse_beats_threshold_and_baseline(self):
        train, test = planted(0)
        mf = MatrixFactorization(n_factors=2, seed=0)
        mf.fit(train, 30, 40)
        mean = np.mean([r for _, _, r in train])
        baseline = float(np.sqrt(np.mean([(mean - r) ** 2 for _, _, r in test])))
        self.assertLess(mf.rmse(test), 0.15)
        self.assertLess(mf.rmse(test), baseline / 3)

    def test_loss_history_decreases(self):
        train, _ = planted(1)
        losses = MatrixFactorization(seed=1, n_epochs=300).fit(train, 30, 40)
        self.assertEqual(len(losses), 300)
        self.assertLess(losses[-1], losses[0] / 20)
        self.assertLessEqual(losses[-1], losses[len(losses) // 2])

    def test_unobserved_cells_are_not_treated_as_zero(self):
        # Every rating is 4. Filling missing cells with 0 would drag unseen predictions toward 2.
        rng = np.random.default_rng(2)
        cells = [(u, i) for u in range(20) for i in range(20)]
        observed = set(rng.choice(len(cells), size=200, replace=False).tolist())
        train = [(u, i, 4.0) for j, (u, i) in enumerate(cells) if j in observed]
        unseen = [(u, i, 4.0) for j, (u, i) in enumerate(cells) if j not in observed]
        mf = MatrixFactorization(n_factors=2, seed=2)
        mf.fit(train, 20, 20)
        self.assertLess(mf.rmse(unseen), 0.1)

    def test_same_seed_same_model(self):
        train, test = planted(3)
        a = MatrixFactorization(seed=7, n_epochs=200)
        b = MatrixFactorization(seed=7, n_epochs=200)
        self.assertEqual(a.fit(train, 30, 40), b.fit(train, 30, 40))
        self.assertEqual([a.predict(u, i) for u, i, _ in test], [b.predict(u, i) for u, i, _ in test])
        c = MatrixFactorization(seed=8, n_epochs=200)
        c.fit(train, 30, 40)
        self.assertNotEqual(a.predict(0, 0), c.predict(0, 0))

    def test_regularization_shrinks_predictions(self):
        train, _ = planted(4)
        weak = MatrixFactorization(reg=0.01, seed=4, n_epochs=500)
        strong = MatrixFactorization(reg=50.0, seed=4, n_epochs=500)
        weak.fit(train, 30, 40)
        strong.fit(train, 30, 40)
        mean_abs = lambda m: np.mean([abs(m.predict(u, i)) for u in range(30) for i in range(40)])
        self.assertLess(mean_abs(strong), 0.8 * mean_abs(weak))

    def test_predict_returns_a_float(self):
        train, _ = planted(5)
        mf = MatrixFactorization(seed=5, n_epochs=50)
        mf.fit(train, 30, 40)
        self.assertIsInstance(mf.predict(0, 0), float)
        self.assertIsInstance(mf.rmse(train[:5]), float)

    def test_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            MatrixFactorization(n_factors=0)
        mf = MatrixFactorization(n_epochs=5)
        with self.assertRaises(ValueError):
            mf.fit([], 3, 3)
        with self.assertRaises(ValueError):
            mf.fit([(3, 0, 4.0)], 3, 3)
        with self.assertRaises(ValueError):
            mf.fit([(0, 5, 4.0)], 3, 3)
        with self.assertRaises(RuntimeError):
            MatrixFactorization().predict(0, 0)

    def test_fast_enough(self):
        train, _ = planted(6)
        start = time.perf_counter()
        MatrixFactorization(seed=6).fit(train, 30, 40)
        self.assertLess(time.perf_counter() - start, 2.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
