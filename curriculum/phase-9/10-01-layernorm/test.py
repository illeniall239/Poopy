import unittest

import torch
import torch.nn.functional as F

from solution import layernorm


class TestLayerNorm(unittest.TestCase):
    def test_hand_computed_rows(self):
        out = layernorm(torch.tensor([[1.0, 2.0, 3.0]]), torch.ones(3), torch.zeros(3))
        self.assertTrue(torch.allclose(out, torch.tensor([[-1.2247, 0.0, 1.2247]]), atol=1e-4))
        out = layernorm(torch.tensor([[1.0, 2.0, 3.0]]), torch.full((3,), 2.0), torch.ones(3))
        self.assertTrue(torch.allclose(out, torch.tensor([[-1.4495, 1.0, 3.4495]]), atol=1e-4))

    def test_each_row_has_mean_zero_and_unit_variance(self):
        torch.manual_seed(0)
        x = torch.randn(6, 8) * 3 + 5
        out = layernorm(x, torch.ones(8), torch.zeros(8))
        self.assertEqual(out.shape, x.shape)
        self.assertTrue(torch.allclose(out.mean(dim=1), torch.zeros(6), atol=1e-5))
        self.assertTrue(torch.allclose(out.var(dim=1, unbiased=False), torch.ones(6), atol=1e-3))

    def test_matches_torch_layer_norm(self):
        torch.manual_seed(1)
        x = torch.randn(5, 7)
        gamma = torch.randn(7)
        beta = torch.randn(7)
        want = F.layer_norm(x, (7,), gamma, beta, 1e-5)
        self.assertTrue(torch.allclose(layernorm(x, gamma, beta), want, atol=1e-5))
        want = F.layer_norm(x, (7,), gamma, beta, 1e-2)
        self.assertTrue(torch.allclose(layernorm(x, gamma, beta, eps=1e-2), want, atol=1e-5))

    def test_rows_are_independent_of_the_batch(self):
        torch.manual_seed(2)
        row = torch.randn(1, 4)
        others = torch.randn(3, 4) * 10 + 100
        alone = layernorm(row, torch.ones(4), torch.zeros(4))
        together = layernorm(torch.cat([others, row]), torch.ones(4), torch.zeros(4))
        self.assertTrue(torch.allclose(alone[0], together[-1], atol=1e-6))
        # Columns are NOT normalized: batch-wise column means are far from zero.
        self.assertGreater(together.mean(dim=0).abs().max().item(), 0.05)

    def test_constant_row_gives_beta_not_nan(self):
        beta = torch.tensor([0.5, -1.0, 2.0, 0.0])
        out = layernorm(torch.full((2, 4), 5.0), torch.ones(4), beta)
        self.assertTrue(torch.allclose(out, beta.expand(2, 4), atol=1e-6))

    def test_works_on_extra_leading_dims(self):
        torch.manual_seed(3)
        x = torch.randn(2, 3, 5)
        gamma, beta = torch.randn(5), torch.randn(5)
        self.assertTrue(torch.allclose(layernorm(x, gamma, beta), F.layer_norm(x, (5,), gamma, beta), atol=1e-5))

    def test_gamma_and_beta_receive_gradients(self):
        torch.manual_seed(4)
        x = torch.randn(3, 4)
        gamma = torch.ones(4, requires_grad=True)
        beta = torch.zeros(4, requires_grad=True)
        (layernorm(x, gamma, beta) * torch.randn(3, 4)).sum().backward()
        self.assertIsNotNone(gamma.grad)
        self.assertIsNotNone(beta.grad)
        self.assertGreater(gamma.grad.abs().sum().item(), 0.0)
        self.assertGreater(beta.grad.abs().sum().item(), 0.0)

    def test_rejects_wrong_parameter_shapes(self):
        x = torch.randn(4, 6)
        with self.assertRaises(ValueError):
            layernorm(x, torch.ones(3), torch.zeros(3))
        with self.assertRaises(ValueError):
            layernorm(x, torch.ones(6), torch.zeros(4))


if __name__ == "__main__":
    unittest.main(verbosity=2)
