import unittest

import torch
from torch import nn

from solution import residual_block_forward, ResidualMLP


class TestResidualBlock(unittest.TestCase):
    def test_list_version_adds_f_of_x(self):
        self.assertEqual(residual_block_forward([1.0, -2.0], lambda v: [0.5, 0.5]), [1.5, -1.5])
        self.assertEqual(residual_block_forward([3.0, 4.0], lambda v: [2 * a for a in v]), [9.0, 12.0])

    def test_list_version_zero_f_is_identity_and_calls_f_once(self):
        calls = []

        def f(v):
            calls.append(1)
            return [0.0] * len(v)

        x = [1.0, -2.0]
        self.assertEqual(residual_block_forward(x, f), [1.0, -2.0])
        self.assertEqual(len(calls), 1)
        self.assertEqual(x, [1.0, -2.0])

    def test_list_version_rejects_length_mismatch(self):
        with self.assertRaises(ValueError):
            residual_block_forward([1.0], lambda v: [1.0, 2.0])

    def test_module_structure(self):
        block = ResidualMLP(4, 8)
        self.assertIsInstance(block.f, nn.Sequential)
        self.assertEqual(len(block.f), 3)
        self.assertEqual((block.f[0].in_features, block.f[0].out_features), (4, 8))
        self.assertIsInstance(block.f[1], nn.ReLU)
        self.assertEqual((block.f[2].in_features, block.f[2].out_features), (8, 4))

    def test_module_output_is_x_plus_f_of_x(self):
        torch.manual_seed(0)
        block = ResidualMLP(4, 8)
        x = torch.randn(5, 4) * 3
        out = block(x)
        self.assertEqual(tuple(out.shape), (5, 4))
        self.assertTrue(torch.allclose(out, x + block.f(x), atol=1e-6))

    def test_no_activation_after_the_add(self):
        block = ResidualMLP(3, 2)
        with torch.no_grad():
            for p in block.f.parameters():
                p.zero_()
        x = torch.tensor([[-1.0, -5.0, 2.0]])
        self.assertTrue(torch.allclose(block(x), x))

    def test_identity_path_gives_gradient_one(self):
        block = ResidualMLP(3, 2)
        with torch.no_grad():
            for p in block.f.parameters():
                p.zero_()
        x = torch.tensor([[-1.0, 0.5, 2.0]], requires_grad=True)
        block(x).sum().backward()
        self.assertTrue(torch.allclose(x.grad, torch.ones_like(x)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
