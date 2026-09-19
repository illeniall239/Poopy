import math
import unittest

import numpy as np
from numpy.testing import assert_allclose

from solution import cross_entropy_from_logits, log_softmax

STRICT = dict(over="raise", divide="raise", invalid="raise")


def naive_ce(z, t):
    p = np.exp(z) / np.exp(z).sum()
    return float(-np.log(p[t]))


class TestCrossEntropyFromLogits(unittest.TestCase):
    def test_small_examples(self):
        self.assertAlmostEqual(cross_entropy_from_logits(np.array([0.0, 0.0]), 0), math.log(2), places=12)
        self.assertAlmostEqual(cross_entropy_from_logits(np.array([1.0, 2.0, 3.0]), 2), 0.4076059644443804, places=12)
        self.assertIsInstance(cross_entropy_from_logits(np.array([1.0, 2.0]), 0), float)

    def test_matches_naive_on_moderate_values(self):
        rng = np.random.default_rng(0)
        for _ in range(50):
            z = rng.normal(scale=5, size=6)
            t = int(rng.integers(0, 6))
            self.assertAlmostEqual(cross_entropy_from_logits(z, t), naive_ce(z, t), delta=1e-10)

    def test_extreme_logits_are_finite(self):
        with np.errstate(**STRICT):
            self.assertAlmostEqual(cross_entropy_from_logits(np.array([1000.0, 0.0]), 1), 1000.0, places=9)
            self.assertEqual(cross_entropy_from_logits(np.array([1000.0, 0.0]), 0), 0.0)
            self.assertAlmostEqual(cross_entropy_from_logits(np.array([-1000.0, -1000.0]), 1), math.log(2), places=12)
            self.assertAlmostEqual(cross_entropy_from_logits(np.array([0.0, 5000.0, -5000.0]), 2), 10000.0, places=6)

    def test_log_softmax(self):
        with np.errstate(**STRICT):
            out = log_softmax(np.array([1000.0, 1001.0]))
        assert_allclose(out, [-1.3132616875182228, -0.31326168751822286], rtol=1e-12)
        rng = np.random.default_rng(1)
        z = rng.normal(scale=3, size=(4, 5))
        ls = log_softmax(z)
        self.assertEqual(ls.shape, (4, 5))
        assert_allclose(np.exp(ls).sum(axis=1), np.ones(4), atol=1e-12)
        assert_allclose(ls, z - np.log(np.exp(z).sum(axis=1, keepdims=True)), atol=1e-12)
        with np.errstate(**STRICT):
            self.assertTrue(np.all(np.isfinite(log_softmax(np.array([[1e4, 0.0, -1e4]])))))

    def test_batch_mean(self):
        z = np.array([[0.0, 0.0], [1000.0, 0.0]])
        with np.errstate(**STRICT):
            loss = cross_entropy_from_logits(z, np.array([0, 1]))
        self.assertAlmostEqual(loss, (math.log(2) + 1000.0) / 2, places=9)
        rng = np.random.default_rng(2)
        z = rng.normal(size=(300, 4))
        t = rng.integers(0, 4, size=300)
        expected = np.mean([naive_ce(z[i], t[i]) for i in range(300)])
        self.assertAlmostEqual(cross_entropy_from_logits(z, t), expected, places=10)

    def test_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            cross_entropy_from_logits(np.array([1.0, 2.0]), 2)
        with self.assertRaises(ValueError):
            cross_entropy_from_logits(np.array([1.0, 2.0]), -1)
        with self.assertRaises(ValueError):
            cross_entropy_from_logits(np.zeros((3, 2)), np.array([0, 1]))
        with self.assertRaises(ValueError):
            cross_entropy_from_logits(np.zeros((2, 2, 2)), np.array([0, 1]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
