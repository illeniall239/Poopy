import random
import unittest

import numpy as np

from solution import fit_polynomial, polynomial_features, solve


def cubic(x):
    return 2 - x + 0.5 * x**2 + 3 * x**3


class TestPolynomialRegression(unittest.TestCase):
    def test_features(self):
        self.assertEqual(polynomial_features([2, 3], 2), [[1, 2, 4], [1, 3, 9]])
        self.assertEqual(polynomial_features([5], 0), [[1]])
        self.assertEqual(polynomial_features([-1.5], 3), [[1, -1.5, 2.25, -3.375]])
        self.assertEqual(polynomial_features([], 2), [])
        with self.assertRaises(ValueError):
            polynomial_features([1, 2], -1)

    def test_solve_still_works(self):
        x = solve([[0, 1], [1, 0]], [5, 7])
        np.testing.assert_allclose(x, [7.0, 5.0], atol=1e-12)
        with self.assertRaises(ValueError):
            solve([[1, 2], [2, 4]], [3, 6])

    def test_line_through_points_needs_the_bias(self):
        np.testing.assert_allclose(fit_polynomial([0, 1, 2], [1, 3, 5], 1), [1.0, 2.0], atol=1e-10)

    def test_recovers_a_cubic_exactly(self):
        xs = [-2, -1, 0, 1, 2, 3]
        coeffs = fit_polynomial(xs, [cubic(x) for x in xs], 3)
        self.assertEqual(len(coeffs), 4)
        np.testing.assert_allclose(coeffs, [2.0, -1.0, 0.5, 3.0], atol=1e-8)

    def test_degree_zero_is_the_mean(self):
        np.testing.assert_allclose(fit_polynomial([1, 2, 3, 4], [5, 1, 4, 2], 0), [3.0], atol=1e-12)

    def test_matches_polyfit_on_noisy_data(self):
        rng = random.Random(0)
        xs = [rng.uniform(-3, 3) for _ in range(200)]
        ys = [cubic(x) + rng.gauss(0, 2) for x in xs]
        for degree in (1, 2, 4, 5):
            ours = fit_polynomial(xs, ys, degree)
            theirs = np.polyfit(xs, ys, degree)[::-1]  # polyfit returns the highest power first
            np.testing.assert_allclose(ours, theirs, atol=1e-6, rtol=1e-6)

    def test_too_few_distinct_points_is_singular(self):
        xs = [0, 0, 1, 1, 2, 2]
        with self.assertRaises(ValueError):
            fit_polynomial(xs, [cubic(x) for x in xs], 3)
        with self.assertRaises(ValueError):
            fit_polynomial([1.0, 2.0, 3.0], [1.0, 2.0], 1)

    def test_interpolating_polynomial_has_zero_training_error(self):
        xs = [-2.0, -1.0, 0.0, 1.0, 2.0]
        ys = [1.0, -1.0, 2.0, 0.0, 3.0]
        coeffs = fit_polynomial(xs, ys, 4)
        preds = [sum(c * x**p for p, c in enumerate(coeffs)) for x in xs]
        np.testing.assert_allclose(preds, ys, atol=1e-8)


if __name__ == "__main__":
    unittest.main(verbosity=2)
