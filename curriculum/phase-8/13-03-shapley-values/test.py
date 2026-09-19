import itertools
import math
import unittest

import numpy as np

from solution import shapley_values


def by_permutations(f, x, b):
    # Ground truth: average marginal contribution over every ordering of the features.
    d = len(x)
    phi = np.zeros(d)
    for order in itertools.permutations(range(d)):
        z = b.copy()
        prev = f(z[None, :])[0]
        for i in order:
            z[i] = x[i]
            cur = f(z[None, :])[0]
            phi[i] += cur - prev
            prev = cur
    return phi / math.factorial(d)


def nonlinear(A):
    return np.sin(A[:, 0]) * A[:, 1] + A[:, 2] ** 2 + 0.5 * A[:, 0] * A[:, 2] * (A[:, 3] if A.shape[1] > 3 else 1.0)


class TestShapleyValues(unittest.TestCase):
    def test_linear_model(self):
        got = shapley_values(lambda A: 3 * A[:, 0] + 2 * A[:, 1], np.array([1.0, 1.0]), np.array([0.0, 0.0]))
        np.testing.assert_allclose(got, [3.0, 2.0], atol=1e-12)
        w = np.array([1.5, -2.0, 0.0, 4.0])
        x = np.array([1.0, 2.0, 3.0, -1.0])
        b = np.array([0.5, 0.5, 0.5, 0.5])
        got = shapley_values(lambda A: A @ w + 7.0, x, b)
        np.testing.assert_allclose(got, w * (x - b), atol=1e-12)

    def test_interaction_is_split_evenly(self):
        got = shapley_values(lambda A: A[:, 0] * A[:, 1], np.array([2.0, 3.0]), np.array([0.0, 0.0]))
        np.testing.assert_allclose(got, [3.0, 3.0], atol=1e-12)

    def test_values_sum_to_the_prediction_difference(self):
        rng = np.random.default_rng(0)
        for d in (1, 2, 3, 4):
            for _ in range(3):
                x, b = rng.normal(size=d), rng.normal(size=d)
                f = lambda A: nonlinear(np.pad(A, ((0, 0), (0, 4 - A.shape[1]))))
                phi = shapley_values(f, x, b)
                self.assertEqual(phi.shape, (d,))
                self.assertAlmostEqual(phi.sum(), f(x[None, :])[0] - f(b[None, :])[0], places=9)

    def test_matches_the_average_over_orderings(self):
        rng = np.random.default_rng(1)
        for d in (3, 4):
            x, b = rng.normal(size=d), rng.normal(size=d)
            f = lambda A: nonlinear(np.pad(A, ((0, 0), (0, 4 - A.shape[1]))))
            np.testing.assert_allclose(shapley_values(f, x, b), by_permutations(f, x, b), atol=1e-9)

    def test_ignored_feature_gets_zero_and_symmetric_features_tie(self):
        f = lambda A: A[:, 0] ** 2
        np.testing.assert_allclose(shapley_values(f, np.array([3.0, 7.0]), np.array([1.0, 0.0])), [8.0, 0.0], atol=1e-12)
        g = lambda A: np.exp(A[:, 0] + A[:, 1]) + A[:, 2]
        phi = shapley_values(g, np.array([0.3, 0.3, 1.0]), np.array([0.0, 0.0, 0.0]))
        self.assertAlmostEqual(phi[0], phi[1], places=12)
        self.assertAlmostEqual(phi[2], 1.0, places=12)

    def test_x_equal_to_background_gives_zeros(self):
        x = np.array([1.0, -2.0, 0.5])
        np.testing.assert_allclose(shapley_values(nonlinear, x, x.copy()), np.zeros(3), atol=1e-12)

    def test_rejects_bad_input(self):
        f = lambda A: A.sum(axis=1)
        with self.assertRaises(ValueError):
            shapley_values(f, np.zeros(5), np.zeros(5))
        with self.assertRaises(ValueError):
            shapley_values(f, np.zeros(3), np.zeros(2))
        with self.assertRaises(ValueError):
            shapley_values(f, np.zeros((1, 3)), np.zeros((1, 3)))
        with self.assertRaises(ValueError):
            shapley_values(f, np.zeros(0), np.zeros(0))


if __name__ == "__main__":
    unittest.main(verbosity=2)
