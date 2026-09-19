import unittest

import numpy as np
from numpy.testing import assert_allclose
from sklearn.linear_model import Lasso

from solution import gd_step_with_l2, soft_threshold


def lasso_problem():
    rng = np.random.default_rng(0)
    X = rng.normal(size=(200, 8))
    w_true = np.array([3.0, -2.0, 0.0, 0.0, 1.5, 0.0, 0.0, 0.0])
    y = X @ w_true + rng.normal(scale=0.1, size=200)
    return X, y


class TestL2AndSoftThreshold(unittest.TestCase):
    def test_l2_step_examples(self):
        assert_allclose(gd_step_with_l2(np.array([1.0, -2.0]), np.zeros(2), 0.1, 1.0), [0.9, -1.8], atol=1e-12)
        assert_allclose(gd_step_with_l2(np.array([1.0]), np.array([2.0]), 0.1, 0.0), [0.8], atol=1e-12)
        assert_allclose(gd_step_with_l2(np.array([2.0]), np.array([1.0]), 0.5, 0.5), [1.0], atol=1e-12)

    def test_soft_threshold_examples(self):
        out = soft_threshold(np.array([3.0, -0.5, 0.2, -4.0]), 1.0)
        assert_allclose(out, [2.0, 0.0, 0.0, -3.0], atol=1e-12)
        out = soft_threshold(np.array([1.0, -1.0, 0.0]), 1.0)
        self.assertTrue(np.all(out == 0.0))
        assert_allclose(soft_threshold(np.array([[2.0, -2.0]]), 0.0), [[2.0, -2.0]])

    def test_inputs_not_mutated(self):
        w = np.array([3.0, -0.5])
        g = np.array([1.0, 1.0])
        gd_step_with_l2(w, g, 0.1, 1.0)
        soft_threshold(w, 1.0)
        assert_allclose(w, [3.0, -0.5])
        assert_allclose(g, [1.0, 1.0])

    def test_l2_shrinks_but_never_zeroes(self):
        w = np.array([1.0, -0.01, 5.0])
        for _ in range(500):
            w = gd_step_with_l2(w, np.zeros(3), 0.1, 0.5)
        self.assertTrue(np.all(w != 0.0))
        self.assertLess(np.max(np.abs(w)), 1e-8)

    def test_l1_gives_exact_zeros(self):
        w = np.array([1.0, -0.01, 5.0])
        for _ in range(500):
            w = soft_threshold(w, 0.05)
        self.assertTrue(np.all(w == 0.0))

    def test_proximal_lasso_matches_sklearn(self):
        X, y = lasso_problem()
        n = len(y)
        alpha = 0.1
        lr = 1.0 / np.linalg.eigvalsh(X.T @ X / n).max()
        w = np.zeros(X.shape[1])
        for _ in range(3000):
            grad = X.T @ (X @ w - y) / n
            w = soft_threshold(w - lr * grad, lr * alpha)
        ref = Lasso(alpha=alpha, fit_intercept=False, tol=1e-12, max_iter=100000).fit(X, y).coef_
        assert_allclose(w, ref, atol=1e-4)
        self.assertTrue(np.all(w[[2, 3, 5, 6, 7]] == 0.0))

    def test_ridge_by_l2_steps_has_no_zeros(self):
        X, y = lasso_problem()
        n = len(y)
        w = np.zeros(X.shape[1])
        for _ in range(3000):
            w = gd_step_with_l2(w, X.T @ (X @ w - y) / n, 0.5, 0.1)
        self.assertTrue(np.all(w != 0.0))
        expected = np.linalg.solve(X.T @ X / n + 0.1 * np.eye(8), X.T @ y / n)
        assert_allclose(w, expected, atol=1e-6)

    def test_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            soft_threshold(np.array([1.0]), -0.1)
        with self.assertRaises(ValueError):
            gd_step_with_l2(np.array([1.0]), np.array([1.0]), 0.1, -1.0)
        with self.assertRaises(ValueError):
            gd_step_with_l2(np.array([1.0]), np.array([1.0]), 0.0, 1.0)
        with self.assertRaises(ValueError):
            gd_step_with_l2(np.array([1.0, 2.0]), np.array([1.0]), 0.1, 1.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
