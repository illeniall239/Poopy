import math
import unittest

import numpy as np

from solution import mle_bernoulli, mle_gaussian, nll_bernoulli


class TestMleAndNll(unittest.TestCase):
    def test_mle_bernoulli(self):
        self.assertAlmostEqual(mle_bernoulli([1, 0, 1, 1]), 0.75)
        self.assertAlmostEqual(mle_bernoulli([0, 0, 0]), 0.0)
        self.assertAlmostEqual(mle_bernoulli([1]), 1.0)
        with self.assertRaises(ValueError):
            mle_bernoulli([])
        with self.assertRaises(ValueError):
            mle_bernoulli([0, 2])

    def test_mle_gaussian(self):
        m, v = mle_gaussian([2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0])
        self.assertAlmostEqual(m, 5.0)
        self.assertAlmostEqual(v, 4.0)
        self.assertEqual(mle_gaussian([3.0]), (3.0, 0.0))
        with self.assertRaises(ValueError):
            mle_gaussian([])

    def test_mle_gaussian_matches_numpy(self):
        rng = np.random.default_rng(0)
        x = rng.normal(loc=-2, scale=3, size=10_000)
        m, v = mle_gaussian(x.tolist())
        self.assertAlmostEqual(m, float(np.mean(x)), places=12)
        self.assertAlmostEqual(v, float(np.var(x, ddof=0)), places=12)
        self.assertNotAlmostEqual(v, float(np.var(x, ddof=1)), places=6)

    def test_nll_values(self):
        self.assertAlmostEqual(nll_bernoulli([1, 0], [0.9, 0.1]), -math.log(0.9), places=12)
        self.assertAlmostEqual(nll_bernoulli([1, 0], [0.5, 0.5]), math.log(2), places=12)
        self.assertAlmostEqual(nll_bernoulli([0], [0.25]), -math.log(0.75), places=12)

    def test_nll_clipping_is_finite(self):
        loss = nll_bernoulli([1], [0.0])
        self.assertTrue(math.isfinite(loss))
        self.assertAlmostEqual(loss, -math.log(1e-12), places=6)
        self.assertAlmostEqual(nll_bernoulli([0], [1.0]), -math.log(1e-12), delta=1e-3)
        self.assertLess(nll_bernoulli([1], [1.0]), 1e-9)

    def test_nll_errors(self):
        with self.assertRaises(ValueError):
            nll_bernoulli([1, 0], [0.5])
        with self.assertRaises(ValueError):
            nll_bernoulli([], [])
        with self.assertRaises(ValueError):
            nll_bernoulli([1], [1.5])
        with self.assertRaises(ValueError):
            nll_bernoulli([2], [0.5])

    def test_nll_equals_bce_formula(self):
        rng = np.random.default_rng(1)
        ys = rng.integers(0, 2, size=500)
        ps = rng.uniform(0.01, 0.99, size=500)
        expected = float(-np.mean(ys * np.log(ps) + (1 - ys) * np.log(1 - ps)))
        self.assertAlmostEqual(nll_bernoulli(ys.tolist(), ps.tolist()), expected, places=12)

    def test_mle_minimizes_nll(self):
        ys = [1, 0, 1, 1, 0, 1, 1, 1, 0, 1]
        p_hat = mle_bernoulli(ys)
        best = nll_bernoulli(ys, [p_hat] * len(ys))
        for p in [p_hat - 0.1, p_hat - 0.01, p_hat + 0.01, p_hat + 0.1]:
            self.assertGreater(nll_bernoulli(ys, [p] * len(ys)), best)

    def test_confident_correct_beats_hesitant_correct(self):
        self.assertLess(nll_bernoulli([1, 0], [0.99, 0.01]), nll_bernoulli([1, 0], [0.51, 0.49]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
