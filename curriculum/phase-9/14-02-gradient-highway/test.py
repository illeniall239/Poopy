import math
import random
import unittest

import torch

from solution import chain_grad, input_grad_norm


def recipe(depth, width, residual, seed):
    torch.manual_seed(seed)
    ws = [torch.randn(width, width) * 0.5 / math.sqrt(width) for _ in range(depth)]
    x = torch.randn(1, width, requires_grad=True)
    h = x
    for W in ws:
        z = torch.tanh(h @ W.T)
        h = h + z if residual else z
    h.sum().backward()
    return x.grad.norm().item()


class TestGradientHighway(unittest.TestCase):
    def test_chain_grad_small_cases(self):
        self.assertAlmostEqual(chain_grad([0.5, 0.5, 0.5], residual=False), 0.125)
        self.assertAlmostEqual(chain_grad([0.5, 0.5, 0.5], residual=True), 3.375)
        self.assertAlmostEqual(chain_grad([2.0, -0.5], residual=True), 1.5)

    def test_chain_grad_empty_is_one(self):
        self.assertEqual(chain_grad([], residual=False), 1.0)
        self.assertEqual(chain_grad([], residual=True), 1.0)

    def test_plain_chain_vanishes_residual_survives(self):
        rng = random.Random(0)
        derivs = [rng.uniform(-0.1, 0.1) for _ in range(50)]
        self.assertLess(abs(chain_grad(derivs, residual=False)), 1e-40)
        self.assertGreater(abs(chain_grad(derivs, residual=True)), 0.1)

    def test_grad_norm_depth_zero(self):
        self.assertAlmostEqual(input_grad_norm(0, 16, False, 0), 4.0, places=5)
        self.assertAlmostEqual(input_grad_norm(0, 9, True, 3), 3.0, places=5)

    def test_grad_norm_follows_the_recipe(self):
        for depth, residual, seed in [(1, False, 0), (2, True, 1), (3, False, 2), (3, True, 5)]:
            want = recipe(depth, 8, residual, seed)
            got = input_grad_norm(depth, 8, residual, seed)
            self.assertAlmostEqual(got, want, delta=1e-5 * max(1.0, want), msg=f"depth={depth} residual={residual}")

    def test_deep_plain_stack_vanishes_residual_stays_alive(self):
        for seed in range(3):
            self.assertLess(input_grad_norm(50, 16, False, seed), 1e-10)
            self.assertGreater(input_grad_norm(50, 16, True, seed), 1.0)

    def test_rejects_bad_sizes(self):
        with self.assertRaises(ValueError):
            input_grad_norm(-1, 4, False, 0)
        with self.assertRaises(ValueError):
            input_grad_norm(3, 0, True, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
