import math
import unittest

import numpy as np
import torch
from numpy.testing import assert_allclose

from solution import cosine_lr, clip_grad_norm


class TestCosineLr(unittest.TestCase):
    def test_key_points(self):
        for step, want in [(0, 0.0), (5, 0.5), (10, 1.0), (55, 0.5), (100, 0.0)]:
            self.assertAlmostEqual(cosine_lr(step, 100, 1.0, 10), want, places=12, msg=f"step {step}")
        self.assertIsInstance(cosine_lr(3, 100, 1.0, 10), float)

    def test_shape_of_the_curve(self):
        self.assertAlmostEqual(cosine_lr(2, 100, 0.4, 8), 0.1, places=12)
        self.assertAlmostEqual(cosine_lr(0, 100, 0.3, 0), 0.3, places=12)
        want = 0.3 * 0.5 * (1 + math.cos(math.pi * 0.25))
        self.assertAlmostEqual(cosine_lr(25, 100, 0.3, 0), want, places=12)
        rates = [cosine_lr(s, 50, 1.0, 5) for s in range(51)]
        self.assertTrue(all(a < b for a, b in zip(rates[:5], rates[1:6])))
        self.assertTrue(all(a > b for a, b in zip(rates[5:50], rates[6:51])))

    def test_rejects_bad_arguments(self):
        for args in [(-1, 100, 1.0, 10), (101, 100, 1.0, 10), (5, 100, 0.0, 10),
                     (5, 100, 1.0, -1), (5, 100, 1.0, 100)]:
            with self.assertRaises(ValueError, msg=str(args)):
                cosine_lr(*args)


class TestClipGradNorm(unittest.TestCase):
    def test_global_norm_not_per_element(self):
        g = [np.array([3.0]), np.array([4.0])]
        self.assertAlmostEqual(clip_grad_norm(g, 1.0), 5.0, places=12)
        assert_allclose(np.concatenate(g), [0.6, 0.8], atol=1e-12)

    def test_under_the_limit_is_unchanged(self):
        g = [np.array([3.0, 4.0])]
        norm = clip_grad_norm(g, 10.0)
        self.assertIsInstance(norm, float)
        self.assertAlmostEqual(norm, 5.0, places=12)
        assert_allclose(g[0], [3.0, 4.0])

    def test_matches_torch_on_mixed_shapes(self):
        rng = np.random.default_rng(0)
        grads = [rng.normal(size=(3, 4)), rng.normal(size=5), rng.normal(size=(2, 2, 2))]
        params = [torch.zeros(g.shape, dtype=torch.float64, requires_grad=True) for g in grads]
        for p, g in zip(params, grads):
            p.grad = torch.tensor(g)
        want_norm = torch.nn.utils.clip_grad_norm_(params, 1.5).item()
        norm = clip_grad_norm(grads, 1.5)
        self.assertAlmostEqual(norm, want_norm, delta=1e-9)
        for g, p in zip(grads, params):
            self.assertEqual(g.shape, tuple(p.shape))
            assert_allclose(g, p.grad.numpy(), rtol=1e-6)
        total = math.sqrt(sum(float((g ** 2).sum()) for g in grads))
        self.assertAlmostEqual(total, 1.5, places=9)

    def test_empty_and_zero_gradients(self):
        self.assertEqual(clip_grad_norm([], 1.0), 0.0)
        g = [np.zeros(3)]
        self.assertEqual(clip_grad_norm(g, 1.0), 0.0)
        assert_allclose(g[0], np.zeros(3))

    def test_rejects_non_positive_max_norm(self):
        with self.assertRaises(ValueError):
            clip_grad_norm([np.array([1.0])], 0.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
