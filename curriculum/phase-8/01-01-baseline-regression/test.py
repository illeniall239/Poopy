import random
import unittest

from solution import baseline_mse, mean_baseline, mse


class TestBaselineRegression(unittest.TestCase):
    def test_mean_baseline_is_the_mean(self):
        self.assertAlmostEqual(mean_baseline([1.0, 2.0, 3.0]), 2.0)
        self.assertAlmostEqual(mean_baseline([5.0]), 5.0)
        self.assertAlmostEqual(mean_baseline([-1.0, 1.0]), 0.0)

    def test_mean_baseline_rejects_empty(self):
        with self.assertRaises(ValueError):
            mean_baseline([])

    def test_mse_of_a_perfect_prediction_is_zero(self):
        self.assertAlmostEqual(mse([1.0, 2.0, 3.0], [1.0, 2.0, 3.0]), 0.0)

    def test_mse_hand_computed(self):
        self.assertAlmostEqual(mse([1.0, 2.0], [2.0, 4.0]), 2.5)
        self.assertAlmostEqual(mse([0.0, 0.0, 0.0], [3.0, -3.0, 0.0]), 6.0)

    def test_mse_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            mse([1.0, 2.0], [1.0])
        with self.assertRaises(ValueError):
            mse([], [])

    def test_baseline_mse_uses_the_train_mean_not_the_val_mean(self):
        # Train mean is 2.0. Using the val mean (3.0) would give 1.0 instead.
        self.assertAlmostEqual(baseline_mse([1.0, 2.0, 3.0], [2.0, 4.0]), 2.0)

    def test_baseline_mse_on_shifted_validation_data_is_large(self):
        rng = random.Random(0)
        train = [rng.gauss(0.0, 1.0) for _ in range(2000)]
        val = [rng.gauss(10.0, 1.0) for _ in range(2000)]
        self.assertGreater(baseline_mse(train, val), 90.0)
        self.assertLess(baseline_mse(train, train), 1.2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
