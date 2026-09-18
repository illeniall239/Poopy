import math
import unittest

import numpy as np

from solution import mean_ci, proportion_ci, sample_size_for_margin


class TestConfidenceIntervals(unittest.TestCase):
    def test_mean_ci_example(self):
        lo, hi = mean_ci([2, 4, 4, 4, 5, 5, 7, 9])
        s = np.std([2, 4, 4, 4, 5, 5, 7, 9], ddof=1)
        self.assertAlmostEqual(lo, 5 - 1.96 * s / math.sqrt(8))
        self.assertAlmostEqual(hi, 5 + 1.96 * s / math.sqrt(8))

    def test_mean_ci_symmetric_and_z_scales_width(self):
        sample = [1.0, 2.0, 3.0, 4.0, 10.0]
        lo, hi = mean_ci(sample, z=1.0)
        self.assertAlmostEqual((lo + hi) / 2, 4.0)
        lo2, hi2 = mean_ci(sample, z=2.0)
        self.assertAlmostEqual(hi2 - lo2, 2 * (hi - lo))

    def test_mean_ci_errors(self):
        with self.assertRaises(ValueError):
            mean_ci([1.0])
        with self.assertRaises(ValueError):
            mean_ci([])

    def test_mean_ci_matches_numpy_random(self):
        rng = np.random.default_rng(0)
        x = rng.normal(loc=10, scale=3, size=5000)
        lo, hi = mean_ci(x.tolist(), z=2.5758)
        half = 2.5758 * x.std(ddof=1) / math.sqrt(len(x))
        self.assertAlmostEqual(lo, x.mean() - half, places=9)
        self.assertAlmostEqual(hi, x.mean() + half, places=9)

    def test_proportion_ci(self):
        lo, hi = proportion_ci(50, 100)
        self.assertAlmostEqual(lo, 0.5 - 1.96 * 0.05)
        self.assertAlmostEqual(hi, 0.5 + 1.96 * 0.05)
        self.assertEqual(proportion_ci(0, 20), (0.0, 0.0))
        self.assertEqual(proportion_ci(100, 100), (1.0, 1.0))

    def test_proportion_ci_clipped(self):
        lo, hi = proportion_ci(1, 10, z=3.0)
        self.assertEqual(lo, 0.0)
        self.assertAlmostEqual(hi, 0.1 + 3.0 * math.sqrt(0.09 / 10))

    def test_proportion_ci_errors(self):
        for s, n in [(5, 0), (-1, 10), (11, 10)]:
            with self.assertRaises(ValueError):
                proportion_ci(s, n)

    def test_sample_size(self):
        self.assertEqual(sample_size_for_margin(0.03), 1068)
        self.assertEqual(sample_size_for_margin(0.05, p=0.1), 139)
        self.assertEqual(sample_size_for_margin(0.01), 9604)
        n = sample_size_for_margin(0.02, z=2.5758)
        self.assertLessEqual(2.5758 * math.sqrt(0.25 / n), 0.02)
        self.assertGreater(2.5758 * math.sqrt(0.25 / (n - 1)), 0.02)

    def test_sample_size_errors(self):
        with self.assertRaises(ValueError):
            sample_size_for_margin(0.0)
        with self.assertRaises(ValueError):
            sample_size_for_margin(0.05, p=1.5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
