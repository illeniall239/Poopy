import math
import unittest

import numpy as np
import torch
import torch.nn.functional as F
from numpy.testing import assert_allclose

from solution import softmax_ce_backward

STRICT = dict(over="raise", divide="raise", invalid="raise")


def torch_reference(logits, targets):
    z = torch.tensor(logits, dtype=torch.float64, requires_grad=True)
    loss = F.cross_entropy(z, torch.tensor(targets, dtype=torch.long))
    loss.backward()
    return loss.item(), z.grad.numpy()


class TestSoftmaxCEBackward(unittest.TestCase):
    def test_two_equal_logits(self):
        loss, d = softmax_ce_backward(np.array([[0.0, 0.0]]), np.array([0]))
        self.assertIsInstance(loss, float)
        self.assertAlmostEqual(loss, math.log(2), places=12)
        assert_allclose(d, [[-0.5, 0.5]], atol=1e-12)

    def test_matches_torch_autograd(self):
        rng = np.random.default_rng(0)
        logits = rng.normal(scale=3.0, size=(6, 5))
        targets = rng.integers(0, 5, size=6)
        loss, d = softmax_ce_backward(logits, targets)
        want_loss, want_d = torch_reference(logits, targets)
        self.assertAlmostEqual(loss, want_loss, delta=1e-9)
        self.assertEqual(d.shape, (6, 5))
        assert_allclose(d, want_d, atol=1e-9)

    def test_gradient_is_divided_by_batch_size(self):
        row, t = np.array([[0.3, -1.2, 2.0]]), np.array([2])
        loss1, d1 = softmax_ce_backward(row, t)
        loss4, d4 = softmax_ce_backward(np.repeat(row, 4, axis=0), np.repeat(t, 4))
        self.assertAlmostEqual(loss1, loss4, places=12)
        assert_allclose(d4, np.repeat(d1, 4, axis=0) / 4, atol=1e-12)

    def test_rows_sum_to_zero(self):
        rng = np.random.default_rng(1)
        _, d = softmax_ce_backward(rng.normal(size=(8, 7)), rng.integers(0, 7, size=8))
        assert_allclose(d.sum(axis=1), np.zeros(8), atol=1e-12)

    def test_extreme_logits_are_stable(self):
        with np.errstate(**STRICT):
            loss, d = softmax_ce_backward(np.array([[1000.0, 0.0], [-1000.0, 1000.0]]), np.array([1, 1]))
        self.assertAlmostEqual(loss, 500.0, places=9)
        assert_allclose(d, [[0.5, -0.5], [0.0, 0.0]], atol=1e-12)

    def test_inputs_are_not_modified(self):
        logits, targets = np.array([[1.0, 2.0, 3.0]]), np.array([0])
        softmax_ce_backward(logits, targets)
        assert_allclose(logits, [[1.0, 2.0, 3.0]])

    def test_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            softmax_ce_backward(np.zeros((2, 3)), np.array([0, 3]))
        with self.assertRaises(ValueError):
            softmax_ce_backward(np.zeros((2, 3)), np.array([0]))
        with self.assertRaises(ValueError):
            softmax_ce_backward(np.zeros(3), np.array([0]))
        with self.assertRaises(ValueError):
            softmax_ce_backward(np.zeros((2, 3)), np.array([-1, 0]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
