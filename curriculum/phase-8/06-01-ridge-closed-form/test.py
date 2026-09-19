import unittest

import numpy as np
from numpy.testing import assert_allclose
from sklearn.linear_model import Ridge

from solution import ridge_closed_form


def make_data(seed, n=200, d=5, offset=100.0):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n, d)) * 3 + 2
    w_true = rng.normal(size=d)
    y = X @ w_true + offset + rng.normal(scale=0.5, size=n)
    return X, y


class TestRidgeClosedForm(unittest.TestCase):
    def test_hand_example(self):
        X = np.array([[1.0], [2.0], [3.0]])
        y = np.array([2.0, 4.0, 6.0])
        w, b = ridge_closed_form(X, y, 0.0)
        assert_allclose(w, [2.0], atol=1e-9)
        self.assertAlmostEqual(b, 0.0, places=9)
        w, b = ridge_closed_form(X, y, 2.0)
        assert_allclose(w, [1.0], atol=1e-9)
        self.assertAlmostEqual(b, 2.0, places=9)

    def test_return_types(self):
        X, y = make_data(0)
        w, b = ridge_closed_form(X, y, 1.0)
        self.assertIsInstance(w, np.ndarray)
        self.assertEqual(w.shape, (5,))
        self.assertIsInstance(b, float)

    def test_lambda_zero_is_least_squares(self):
        X, y = make_data(1)
        A = np.column_stack([X, np.ones(len(X))])
        coef, *_ = np.linalg.lstsq(A, y, rcond=None)
        w, b = ridge_closed_form(X, y, 0.0)
        assert_allclose(w, coef[:-1], atol=1e-6)
        self.assertAlmostEqual(b, coef[-1], places=6)

    def test_matches_sklearn_ridge(self):
        X, y = make_data(2)
        for lam in [0.1, 10.0, 1000.0]:
            model = Ridge(alpha=lam).fit(X, y)
            w, b = ridge_closed_form(X, y, lam)
            assert_allclose(w, model.coef_, atol=1e-6)
            self.assertAlmostEqual(b, model.intercept_, places=6)

    def test_weights_shrink_monotonically(self):
        X, y = make_data(3)
        norms = [np.linalg.norm(ridge_closed_form(X, y, lam)[0]) for lam in [0.0, 0.1, 1.0, 10.0, 100.0, 1e4, 1e6]]
        for a, b in zip(norms, norms[1:]):
            self.assertLess(b, a)

    def test_bias_is_not_penalized(self):
        # With a huge lam, w -> 0 and the prediction must fall back to mean(y) (~100), not to 0.
        X, y = make_data(4, offset=100.0)
        w, b = ridge_closed_form(X, y, 1e10)
        self.assertLess(np.linalg.norm(w), 1e-4)
        self.assertAlmostEqual(b, y.mean(), places=3)

    def test_rejects_bad_input(self):
        X, y = make_data(5)
        with self.assertRaises(ValueError):
            ridge_closed_form(X, y, -1.0)
        with self.assertRaises(ValueError):
            ridge_closed_form(X, y[:-1], 1.0)
        with self.assertRaises(ValueError):
            ridge_closed_form(X[:, 0], y, 1.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
