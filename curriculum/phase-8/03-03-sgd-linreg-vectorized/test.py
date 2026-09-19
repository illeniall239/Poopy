import unittest

import numpy as np

from solution import normal_equation, sgd_linreg

TRUE_W = np.array([0.003, 200.0, -1.5])
TRUE_B = 4.0


def data(n, noise, seed):
    rng = np.random.default_rng(seed)
    X = np.column_stack([
        rng.uniform(0, 1000, n),      # thousands
        rng.normal(0, 0.01, n),       # hundredths
        rng.uniform(-5, 5, n),
    ])
    y = X @ TRUE_W + TRUE_B + rng.normal(0, noise, n)
    return X, y


class TestSgdLinregVectorized(unittest.TestCase):
    def test_normal_equation_matches_lstsq(self):
        X, y = data(300, 0.5, seed=0)
        w, b = normal_equation(X, y)
        theta, *_ = np.linalg.lstsq(np.column_stack([np.ones(len(X)), X]), y, rcond=None)
        np.testing.assert_allclose(w, theta[1:], rtol=1e-8)
        self.assertAlmostEqual(b, theta[0], places=6)
        self.assertIsInstance(b, float)
        self.assertEqual(w.shape, (3,))

    def test_noiseless_sgd_reaches_the_closed_form(self):
        X, y = data(500, 0.0, seed=1)
        w, b, hist = sgd_linreg(X, y, 0.05, 30, 16, seed=0)
        w_ne, b_ne = normal_equation(X, y)
        np.testing.assert_allclose(w, w_ne, rtol=1e-6)
        self.assertAlmostEqual(b, b_ne, delta=1e-6 * max(1.0, abs(b_ne)))
        self.assertIsInstance(b, float)
        self.assertEqual(len(hist), 30)
        self.assertLess(hist[-1], 1e-10)

    def test_noisy_sgd_lands_near_the_closed_form(self):
        X, y = data(2000, 0.5, seed=2)
        w, b, hist = sgd_linreg(X, y, 0.01, 20, 32, seed=0)
        w_ne, b_ne = normal_equation(X, y)
        sigma = X.std(axis=0)
        # Compare in standardized units so every feature counts equally.
        np.testing.assert_allclose(w * sigma, w_ne * sigma, atol=0.02)
        ne_mse = np.mean((X @ w_ne + b_ne - y) ** 2)
        self.assertLess(hist[-1], ne_mse * 1.01)
        self.assertAlmostEqual(hist[-1], float(np.mean((X @ w + b - y) ** 2)), places=9)

    def test_loss_falls(self):
        X, y = data(500, 0.5, seed=3)
        _, _, hist = sgd_linreg(X, y, 0.02, 10, 16, seed=0)
        self.assertTrue(all(np.isfinite(hist)))
        self.assertLess(hist[-1], hist[0] / 10)

    def test_deterministic_and_actually_shuffled(self):
        X, y = data(400, 0.5, seed=4)
        a = sgd_linreg(X, y, 0.02, 5, 16, seed=7)
        b = sgd_linreg(X, y, 0.02, 5, 16, seed=7)
        np.testing.assert_array_equal(a[0], b[0])
        self.assertEqual(a[2], b[2])
        c = sgd_linreg(X, y, 0.02, 5, 16, seed=8)
        self.assertNotEqual(a[2], c[2])

    def test_batch_size_larger_than_n_is_full_batch(self):
        X, y = data(50, 0.0, seed=5)
        w, b, _ = sgd_linreg(X, y, 0.1, 300, 1000, seed=0)
        w_ne, b_ne = normal_equation(X, y)
        np.testing.assert_allclose(w, w_ne, rtol=1e-6)

    def test_does_not_modify_inputs(self):
        X, y = data(100, 0.5, seed=6)
        X0, y0 = X.copy(), y.copy()
        sgd_linreg(X, y, 0.02, 2, 16, seed=0)
        np.testing.assert_array_equal(X, X0)
        np.testing.assert_array_equal(y, y0)

    def test_rejects_bad_input(self):
        X, y = data(20, 0.5, seed=7)
        with self.assertRaises(ValueError):
            sgd_linreg(X, y[:-1], 0.01, 1, 4, seed=0)
        with self.assertRaises(ValueError):
            sgd_linreg(X[:, 0], y, 0.01, 1, 4, seed=0)
        constant = X.copy()
        constant[:, 1] = 3.0
        with self.assertRaises(ValueError):
            sgd_linreg(constant, y, 0.01, 1, 4, seed=0)
        with self.assertRaises(ValueError):
            normal_equation(X, y[:-1])


if __name__ == "__main__":
    unittest.main(verbosity=2)
