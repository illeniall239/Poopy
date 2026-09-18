import math
import random
import unittest

import numpy as np

from solution import bootstrap_diff_ci, permutation_test, two_proportion_ztest


class TestABTest(unittest.TestCase):
    def test_ztest_known_case(self):
        z, p = two_proportion_ztest(200, 1000, 250, 1000)
        pooled = 450 / 2000
        se = math.sqrt(pooled * (1 - pooled) * (2 / 1000))
        self.assertAlmostEqual(z, 0.05 / se, places=9)
        self.assertAlmostEqual(p, math.erfc(abs(z) / math.sqrt(2)), places=12)
        self.assertLess(p, 0.01)

    def test_ztest_sign_and_symmetry(self):
        z1, p1 = two_proportion_ztest(200, 1000, 250, 1000)
        z2, p2 = two_proportion_ztest(250, 1000, 200, 1000)
        self.assertAlmostEqual(z1, -z2)
        self.assertAlmostEqual(p1, p2)

    def test_ztest_no_difference_and_degenerate(self):
        self.assertEqual(two_proportion_ztest(200, 1000, 200, 1000), (0.0, 1.0))
        self.assertEqual(two_proportion_ztest(0, 100, 0, 100), (0.0, 1.0))
        self.assertEqual(two_proportion_ztest(100, 100, 50, 50), (0.0, 1.0))

    def test_ztest_errors(self):
        for args in [(1, 0, 1, 10), (11, 10, 1, 10), (-1, 10, 1, 10)]:
            with self.assertRaises(ValueError):
                two_proportion_ztest(*args)

    def test_ztest_p_in_unit_interval(self):
        for s_a, s_b in [(10, 12), (500, 520), (1, 999)]:
            _, p = two_proportion_ztest(s_a, 1000, s_b, 1000)
            self.assertGreaterEqual(p, 0.0)
            self.assertLessEqual(p, 1.0)

    def test_permutation_identical_groups(self):
        p = permutation_test([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], 999, random.Random(0))
        self.assertAlmostEqual(p, 1.0, delta=0.05)

    def test_permutation_clear_difference(self):
        p = permutation_test([1, 2, 3, 4, 5], [11, 12, 13, 14, 15], 999, random.Random(0))
        self.assertLess(p, 0.01)
        self.assertGreaterEqual(p, 1 / 1000)

    def test_permutation_deterministic_and_agrees_with_normal(self):
        rng = np.random.default_rng(0)
        a = rng.normal(0.0, 1.0, size=200).tolist()
        b = rng.normal(0.25, 1.0, size=200).tolist()
        p1 = permutation_test(a, b, 2000, random.Random(1))
        p2 = permutation_test(a, b, 2000, random.Random(1))
        self.assertEqual(p1, p2)
        diff = np.mean(b) - np.mean(a)
        se = math.sqrt(np.var(a, ddof=1) / 200 + np.var(b, ddof=1) / 200)
        p_normal = math.erfc(abs(diff) / se / math.sqrt(2))
        self.assertAlmostEqual(p1, p_normal, delta=0.03)

    def test_bootstrap_interval(self):
        rng = np.random.default_rng(2)
        a = rng.normal(5.0, 2.0, size=300).tolist()
        b = rng.normal(6.0, 2.0, size=300).tolist()
        lo, hi = bootstrap_diff_ci(a, b, 2000, random.Random(0))
        observed = np.mean(b) - np.mean(a)
        self.assertLess(lo, observed)
        self.assertGreater(hi, observed)
        self.assertLess(lo, 1.0)
        self.assertGreater(hi, 1.0)
        se = math.sqrt(np.var(a, ddof=1) / 300 + np.var(b, ddof=1) / 300)
        self.assertAlmostEqual(hi - lo, 2 * 1.96 * se, delta=0.15)
        lo2, hi2 = bootstrap_diff_ci(a, b, 2000, random.Random(0))
        self.assertEqual((lo, hi), (lo2, hi2))
        lo90, hi90 = bootstrap_diff_ci(a, b, 2000, random.Random(0), alpha=0.10)
        self.assertLess(hi90 - lo90, hi - lo)


if __name__ == "__main__":
    unittest.main(verbosity=2)
