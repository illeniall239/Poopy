import math
import unittest

import numpy as np

from solution import expected_initial_ce, too_confident_at_init

STRICT = dict(over="raise", divide="raise", invalid="raise")


class TestExpectedInitialLoss(unittest.TestCase):
    def test_expected_initial_ce(self):
        self.assertAlmostEqual(expected_initial_ce(10), math.log(10), places=12)
        self.assertAlmostEqual(expected_initial_ce(2), math.log(2), places=12)
        self.assertIsInstance(expected_initial_ce(27), float)
        with self.assertRaises(ValueError):
            expected_initial_ce(1)

    def test_uniform_logits_are_fine(self):
        result = too_confident_at_init(np.zeros((4, 10)), 0.1)
        self.assertIs(type(result), bool)
        self.assertFalse(result)
        self.assertFalse(too_confident_at_init(np.full((3, 5), 7.0), 0.0))

    def test_worked_rows(self):
        self.assertTrue(too_confident_at_init(np.array([[0.0, 4.0]]), 0.5))
        self.assertFalse(too_confident_at_init(np.array([[0.0, 0.2]]), 0.5))

    def test_threshold_uses_the_label_average(self):
        # Averaged loss of [0, 4] is logsumexp - 2 = 2.01815; log 2 = 0.69315, gap 1.325.
        row = np.array([[0.0, 4.0]])
        self.assertTrue(too_confident_at_init(row, 1.32))
        self.assertFalse(too_confident_at_init(row, 1.33))

    def test_mean_over_rows(self):
        # One uniform row (loss log 3) and one confident row: only their mean counts.
        rows = np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 6.0]])
        lse = np.log(np.exp(rows).sum(axis=1))
        gap = float(np.mean(lse - rows.mean(axis=1))) - math.log(3)
        self.assertTrue(too_confident_at_init(rows, gap - 1e-6))
        self.assertFalse(too_confident_at_init(rows, gap + 1e-6))

    def test_scale_of_random_init(self):
        rng = np.random.default_rng(0)
        base = rng.standard_normal((256, 10))
        self.assertFalse(too_confident_at_init(0.01 * base, 0.1))
        self.assertTrue(too_confident_at_init(10.0 * base, 0.1))

    def test_extreme_logits_do_not_overflow(self):
        with np.errstate(**STRICT):
            self.assertTrue(too_confident_at_init(np.array([[1000.0, -1000.0]]), 1.0))
            self.assertFalse(too_confident_at_init(np.array([[1000.0, 1000.0]]), 0.0))

    def test_rejects_bad_input(self):
        for logits, tol in [(np.zeros(5), 0.1), (np.zeros((0, 3)), 0.1), (np.zeros((2, 1)), 0.1), (np.zeros((2, 3)), -0.1)]:
            with self.assertRaises(ValueError):
                too_confident_at_init(logits, tol)


if __name__ == "__main__":
    unittest.main(verbosity=2)
