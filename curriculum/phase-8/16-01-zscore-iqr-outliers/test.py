import random
import unittest

import numpy as np

from solution import iqr_flags, zscore_flags

DATA = [1.0, 2.0, 3.0, 4.0, 5.0, 100.0]


class TestZscoreIqrOutliers(unittest.TestCase):
    def test_zscore_hand_computed(self):
        self.assertEqual(zscore_flags(DATA, k=2.0), [False] * 5 + [True])

    def test_zscore_masking_at_k3(self):
        # The 100 inflates the std it is measured against: z ≈ 2.23 < 3.
        self.assertEqual(zscore_flags(DATA, k=3.0), [False] * 6)
        self.assertEqual(zscore_flags(DATA), [False] * 6)

    def test_zscore_uses_population_std(self):
        xs = [10.0, 12.0, 11.0, 13.0, 12.0, 11.0, 50.0]
        # population z of 50 ≈ 2.444, sample z ≈ 2.263
        self.assertEqual(zscore_flags(xs, k=2.3), [False] * 6 + [True])

    def test_iqr_catches_what_zscore_masks(self):
        self.assertEqual(iqr_flags(DATA), [False] * 5 + [True])
        self.assertEqual(iqr_flags([-100.0] + DATA[:5]), [True] + [False] * 5)

    def test_iqr_boundary_is_not_flagged(self):
        # Q1 = 2.25, Q3 = 4.75, IQR = 2.5: fences at -1.5 and 8.5 exactly.
        self.assertEqual(iqr_flags([1.0, 2.0, 3.0, 4.0, 5.0, 8.5]), [False] * 6)
        self.assertEqual(iqr_flags([1.0, 2.0, 3.0, 4.0, 5.0, 8.6]), [False] * 5 + [True])

    def test_constant_and_single_values(self):
        self.assertEqual(zscore_flags([7.0, 7.0, 7.0]), [False] * 3)
        self.assertEqual(iqr_flags([7.0, 7.0, 7.0]), [False] * 3)
        self.assertEqual(zscore_flags([3.0]), [False])
        self.assertEqual(iqr_flags([3.0]), [False])

    def test_empty_raises(self):
        with self.assertRaises(ValueError):
            zscore_flags([])
        with self.assertRaises(ValueError):
            iqr_flags([])

    def test_matches_numpy_on_random_data(self):
        rng = random.Random(3)
        for _ in range(20):
            xs = [rng.gauss(0, 1) for _ in range(rng.randint(2, 40))] + [rng.uniform(-8, 8)]
            rng.shuffle(xs)
            a = np.array(xs)
            z = np.abs(a - a.mean()) / a.std()
            self.assertEqual(zscore_flags(xs, 2.0), list(z > 2.0))
            q1, q3 = np.percentile(a, [25, 75])
            expected = (a < q1 - 1.5 * (q3 - q1)) | (a > q3 + 1.5 * (q3 - q1))
            self.assertEqual(iqr_flags(xs), [bool(v) for v in expected])


if __name__ == "__main__":
    unittest.main(verbosity=2)
