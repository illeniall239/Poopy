import math
import unittest

import numpy as np
from numpy.testing import assert_allclose

from solution import bce_with_logits, bce_with_logits_grad

STRICT = dict(over="raise", divide="raise", invalid="raise")


def naive_bce(z, y):
    p = 1.0 / (1.0 + np.exp(-z))
    return float(np.mean(-(y * np.log(p) + (1 - y) * np.log(1 - p))))


class TestBCEWithLogits(unittest.TestCase):
    def test_log_two_at_zero(self):
        self.assertAlmostEqual(bce_with_logits(np.array([0.0]), np.array([1.0])), math.log(2), places=12)
        self.assertIsInstance(bce_with_logits(np.array([0.0]), np.array([0.0])), float)

    def test_matches_naive_on_moderate_values(self):
        rng = np.random.default_rng(0)
        z = rng.uniform(-20, 20, size=500)
        y = rng.integers(0, 2, size=500).astype(float)
        self.assertAlmostEqual(bce_with_logits(z, y), naive_bce(z, y), delta=1e-10)
        soft = rng.uniform(0, 1, size=500)
        self.assertAlmostEqual(bce_with_logits(z, soft), naive_bce(z, soft), delta=1e-10)

    def test_extreme_logits_are_finite_and_exact(self):
        with np.errstate(**STRICT):
            self.assertAlmostEqual(bce_with_logits(np.array([1000.0]), np.array([0.0])), 1000.0, places=9)
            self.assertAlmostEqual(bce_with_logits(np.array([-1000.0]), np.array([1.0])), 1000.0, places=9)
            self.assertEqual(bce_with_logits(np.array([1000.0]), np.array([1.0])), 0.0)
            self.assertEqual(bce_with_logits(np.array([-1000.0]), np.array([0.0])), 0.0)
            mixed = bce_with_logits(np.array([-1000.0, 2.0]), np.array([1.0, 1.0]))
        self.assertAlmostEqual(mixed, (1000.0 + math.log1p(math.exp(-2.0))) / 2, places=9)

    def test_tiny_losses_keep_precision(self):
        # log(1 + e^-40) is about 4.25e-18; log(1 + x) would round it to exactly 0.
        loss = bce_with_logits(np.array([40.0]), np.array([1.0]))
        self.assertGreater(loss, 0.0)
        self.assertAlmostEqual(loss / math.exp(-40.0), 1.0, places=9)

    def test_gradient_values(self):
        assert_allclose(bce_with_logits_grad(np.array([0.0, 0.0]), np.array([1.0, 0.0])), [-0.25, 0.25], atol=1e-12)
        with np.errstate(**STRICT):
            g = bce_with_logits_grad(np.array([1000.0, -1000.0]), np.array([0.0, 0.0]))
        assert_allclose(g, [0.5, 0.0], atol=1e-12)

    def test_gradient_matches_finite_differences(self):
        rng = np.random.default_rng(1)
        z = rng.uniform(-5, 5, size=(4, 3))
        y = rng.integers(0, 2, size=(4, 3)).astype(float)
        g = bce_with_logits_grad(z, y)
        self.assertEqual(g.shape, (4, 3))
        h = 1e-6
        numeric = np.zeros_like(z)
        for idx in np.ndindex(z.shape):
            zp, zm = z.copy(), z.copy()
            zp[idx] += h
            zm[idx] -= h
            numeric[idx] = (bce_with_logits(zp, y) - bce_with_logits(zm, y)) / (2 * h)
        assert_allclose(g, numeric, atol=1e-6)

    def test_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            bce_with_logits(np.array([1.0, 2.0]), np.array([1.0]))
        with self.assertRaises(ValueError):
            bce_with_logits(np.array([]), np.array([]))
        with self.assertRaises(ValueError):
            bce_with_logits_grad(np.array([1.0, 2.0]), np.array([1.0]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
