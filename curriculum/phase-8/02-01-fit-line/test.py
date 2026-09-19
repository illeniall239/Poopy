import random
import unittest

import numpy as np

from solution import fit_line


class TestFitLine(unittest.TestCase):
    def test_exact_line(self):
        w, b = fit_line([0, 1, 2], [1, 3, 5])
        self.assertAlmostEqual(w, 2.0, places=10)
        self.assertAlmostEqual(b, 1.0, places=10)

    def test_flat_line(self):
        w, b = fit_line([1, 2, 3, 4], [2, 2, 2, 2])
        self.assertAlmostEqual(w, 0.0, places=10)
        self.assertAlmostEqual(b, 2.0, places=10)

    def test_hand_computed_noisy(self):
        w, b = fit_line([0, 1, 2, 3], [1, 0, 2, 1])
        self.assertAlmostEqual(w, 0.2, places=10)
        self.assertAlmostEqual(b, 0.7, places=10)

    def test_large_intercept_is_not_forgotten(self):
        xs = [float(i) for i in range(10)]
        ys = [2.0 * x + 100.0 for x in xs]
        w, b = fit_line(xs, ys)
        self.assertAlmostEqual(w, 2.0, places=9)
        self.assertAlmostEqual(b, 100.0, places=8)

    def test_matches_polyfit(self):
        rng = random.Random(0)
        for n in (2, 5, 50, 2000):
            xs = [rng.uniform(-50, 50) for _ in range(n)]
            ys = [-3.5 * x + 7.0 + rng.gauss(0, 10) for x in xs]
            w, b = fit_line(xs, ys)
            w_np, b_np = np.polyfit(xs, ys, 1)
            self.assertTrue(np.isclose(w, w_np, rtol=1e-8, atol=1e-10), (n, w, w_np))
            self.assertTrue(np.isclose(b, b_np, rtol=1e-8, atol=1e-8), (n, b, b_np))

    def test_residuals_sum_to_zero(self):
        rng = random.Random(1)
        xs = [rng.uniform(0, 10) for _ in range(100)]
        ys = [x * x + rng.gauss(0, 1) for x in xs]
        w, b = fit_line(xs, ys)
        residuals = [y - (w * x + b) for x, y in zip(xs, ys)]
        self.assertAlmostEqual(sum(residuals), 0.0, places=7)
        self.assertAlmostEqual(sum(r * x for r, x in zip(residuals, xs)), 0.0, places=6)

    def test_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            fit_line([3, 3, 3], [1, 2, 3])
        with self.assertRaises(ValueError):
            fit_line([0.1, 0.1, 0.1], [1, 2, 3])  # the float mean is not exactly 0.1
        with self.assertRaises(ValueError):
            fit_line([1.0], [2.0])
        with self.assertRaises(ValueError):
            fit_line([], [])
        with self.assertRaises(ValueError):
            fit_line([1, 2, 3], [1, 2])


if __name__ == "__main__":
    unittest.main(verbosity=2)
