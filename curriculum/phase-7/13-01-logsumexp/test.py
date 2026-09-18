import math
import unittest

import numpy as np
from numpy.testing import assert_allclose

from solution import log_softmax, logsumexp, softmax


class TestLogSumExp(unittest.TestCase):
    def test_moderate_matches_naive(self):
        for xs in [[0.0, 0.0], [5.0], [1.0, 2.0, 3.0], [-3.0, 0.5, 2.2, 1.1]]:
            naive = math.log(sum(math.exp(x) for x in xs))
            self.assertAlmostEqual(logsumexp(xs), naive, places=12)

    def test_large_and_small_inputs(self):
        self.assertAlmostEqual(logsumexp([1000.0, 1000.0]), 1000.0 + math.log(2), places=9)
        self.assertAlmostEqual(logsumexp([-1000.0, -1000.0]), -1000.0 + math.log(2), places=9)
        self.assertAlmostEqual(logsumexp([1000.0, 0.0]), 1000.0, places=9)
        self.assertTrue(math.isfinite(logsumexp([-1e5, -1e5, -1e5])))

    def test_shift_invariance(self):
        xs = [0.3, -1.2, 2.5]
        self.assertAlmostEqual(logsumexp([x + 1000 for x in xs]), logsumexp(xs) + 1000, places=9)

    def test_empty_raises(self):
        with self.assertRaises(ValueError):
            logsumexp([])

    def test_log_softmax_values(self):
        out = log_softmax([1.0, 2.0, 3.0])
        lse = math.log(math.e + math.e**2 + math.e**3)
        assert_allclose(out, [1 - lse, 2 - lse, 3 - lse], atol=1e-12)
        self.assertAlmostEqual(sum(math.exp(v) for v in out), 1.0, places=12)

    def test_softmax_values_and_stability(self):
        assert_allclose(softmax([1.0, 1.0, 1.0]), [1 / 3] * 3, atol=1e-12)
        out = softmax([1000.0, 0.0])
        assert_allclose(out, [1.0, 0.0], atol=1e-12)
        out = softmax([-1000.0, -1000.0, -1000.0])
        assert_allclose(out, [1 / 3] * 3, atol=1e-12)
        self.assertEqual(log_softmax([1000.0, 0.0])[1], -1000.0)

    def test_matches_numpy_random(self):
        rng = np.random.default_rng(0)
        for n in [2, 10, 1000]:
            xs = rng.normal(scale=5, size=n)
            m = xs.max()
            expected_lse = float(m + np.log(np.exp(xs - m).sum()))
            self.assertAlmostEqual(logsumexp(xs.tolist()), expected_lse, places=10)
            p = np.exp(xs - m) / np.exp(xs - m).sum()
            assert_allclose(softmax(xs.tolist()), p, atol=1e-12)
            assert_allclose(log_softmax(xs.tolist()), np.log(p), atol=1e-9)

    def test_softmax_is_a_distribution(self):
        rng = np.random.default_rng(1)
        for _ in range(5):
            p = softmax(rng.normal(scale=50, size=20).tolist())
            self.assertAlmostEqual(sum(p), 1.0, places=12)
            self.assertTrue(all(0.0 <= v <= 1.0 for v in p))


if __name__ == "__main__":
    unittest.main(verbosity=2)
