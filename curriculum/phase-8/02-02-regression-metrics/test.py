import random
import unittest

from sklearn import metrics

from solution import mae, mse, r2, rmse


class TestRegressionMetrics(unittest.TestCase):
    def test_hand_computed(self):
        t, p = [1, 2, 3], [1, 2, 5]
        self.assertAlmostEqual(mse(t, p), 4 / 3, places=12)
        self.assertAlmostEqual(mae(t, p), 2 / 3, places=12)
        self.assertAlmostEqual(rmse(t, p), (4 / 3) ** 0.5, places=12)

    def test_r2_perfect_mean_and_worse(self):
        self.assertAlmostEqual(r2([1, 2, 3], [1, 2, 3]), 1.0, places=12)
        self.assertAlmostEqual(r2([1, 2, 3], [2, 2, 2]), 0.0, places=12)
        self.assertAlmostEqual(r2([1, 2, 3], [3, 2, 1]), -3.0, places=12)

    def test_r2_of_a_constant_that_is_not_the_mean_is_negative(self):
        # Predicting 10 everywhere: SS_res = 81 + 64 + 49 = 194, SS_tot = 2.
        self.assertAlmostEqual(r2([1, 2, 3], [10, 10, 10]), 1 - 194 / 2, places=10)

    def test_outlier_sensitivity(self):
        t = [0.0] * 100
        p = [1.0] * 99 + [100.0]
        self.assertAlmostEqual(mae(t, p), 1.99, places=10)
        self.assertAlmostEqual(mse(t, p), 100.99, places=10)
        self.assertAlmostEqual(rmse(t, p), 100.99 ** 0.5, places=10)

    def test_matches_sklearn(self):
        rng = random.Random(0)
        t = [rng.gauss(50, 20) for _ in range(5000)]
        p = [y + rng.gauss(0, 8) for y in t]
        self.assertAlmostEqual(mse(t, p), metrics.mean_squared_error(t, p), places=9)
        self.assertAlmostEqual(mae(t, p), metrics.mean_absolute_error(t, p), places=9)
        self.assertAlmostEqual(rmse(t, p), metrics.mean_squared_error(t, p) ** 0.5, places=9)
        self.assertAlmostEqual(r2(t, p), metrics.r2_score(t, p), places=9)

    def test_r2_is_not_symmetric(self):
        t = [1.0, 2.0, 3.0, 4.0]
        p = [1.0, 1.0, 1.0, 5.0]
        self.assertAlmostEqual(r2(t, p), metrics.r2_score(t, p), places=12)
        self.assertNotAlmostEqual(r2(t, p), r2(p, t), places=3)

    def test_rejects_bad_input(self):
        for fn in (mse, mae, rmse, r2):
            with self.assertRaises(ValueError):
                fn([], [])
            with self.assertRaises(ValueError):
                fn([1.0, 2.0], [1.0])
        with self.assertRaises(ValueError):
            r2([5.0, 5.0, 5.0], [5.0, 5.0, 5.0])
        with self.assertRaises(ValueError):
            r2([0.1, 0.1, 0.1], [0.0, 0.0, 0.0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
