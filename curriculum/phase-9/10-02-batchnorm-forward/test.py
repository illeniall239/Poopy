import unittest

import torch
from torch import nn

from solution import batchnorm_forward


def fresh_running(d):
    return {"mean": torch.zeros(d), "var": torch.ones(d)}


class TestBatchNormForward(unittest.TestCase):
    def test_hand_computed_training_step(self):
        batch = torch.tensor([[1.0, 10.0], [3.0, 30.0]])
        running = fresh_running(2)
        out = batchnorm_forward(batch, torch.ones(2), torch.zeros(2), running, 0.1, True)
        self.assertTrue(torch.allclose(out, torch.tensor([[-1.0, -1.0], [1.0, 1.0]]), atol=1e-4))
        self.assertTrue(torch.allclose(running["mean"], torch.tensor([0.2, 2.0]), atol=1e-6))
        self.assertTrue(torch.allclose(running["var"], torch.tensor([1.1, 20.9]), atol=1e-5))

    def test_training_normalizes_columns_over_the_batch(self):
        torch.manual_seed(0)
        batch = torch.randn(16, 5) * 4 - 7
        out = batchnorm_forward(batch, torch.ones(5), torch.zeros(5), fresh_running(5))
        self.assertEqual(out.shape, (16, 5))
        self.assertTrue(torch.allclose(out.mean(dim=0), torch.zeros(5), atol=1e-5))
        self.assertTrue(torch.allclose(out.var(dim=0, unbiased=False), torch.ones(5), atol=1e-3))
        # Rows are NOT normalized: the per-row means are not all zero.
        self.assertGreater(out.mean(dim=1).abs().max().item(), 0.05)

    def test_matches_torch_in_training_including_running_stats(self):
        torch.manual_seed(1)
        d, momentum = 4, 0.3
        bn = nn.BatchNorm1d(d, eps=1e-5, momentum=momentum)
        with torch.no_grad():
            bn.weight.copy_(torch.randn(d))
            bn.bias.copy_(torch.randn(d))
        gamma, beta = bn.weight.detach().clone(), bn.bias.detach().clone()
        running = fresh_running(d)
        bn.train()
        for _ in range(3):
            batch = torch.randn(8, d) * 2 + 1
            got = batchnorm_forward(batch, gamma, beta, running, momentum, True)
            self.assertTrue(torch.allclose(got, bn(batch), atol=1e-5))
        self.assertTrue(torch.allclose(running["mean"], bn.running_mean, atol=1e-5))
        self.assertTrue(torch.allclose(running["var"], bn.running_var, atol=1e-5))

    def test_eval_uses_running_stats_and_leaves_them_unchanged(self):
        torch.manual_seed(2)
        running = {"mean": torch.tensor([1.0, -2.0, 0.5]), "var": torch.tensor([4.0, 0.25, 1.0])}
        bn = nn.BatchNorm1d(3)
        with torch.no_grad():
            bn.running_mean.copy_(running["mean"])
            bn.running_var.copy_(running["var"])
        bn.eval()
        batch = torch.randn(6, 3) * 3
        got = batchnorm_forward(batch, torch.ones(3), torch.zeros(3), running, 0.1, False)
        self.assertTrue(torch.allclose(got, bn(batch), atol=1e-5))
        self.assertTrue(torch.equal(running["mean"], torch.tensor([1.0, -2.0, 0.5])))
        self.assertTrue(torch.equal(running["var"], torch.tensor([4.0, 0.25, 1.0])))

    def test_gamma_scales_and_beta_shifts(self):
        torch.manual_seed(3)
        batch = torch.randn(10, 3)
        gamma = torch.tensor([2.0, -1.0, 0.5])
        beta = torch.tensor([1.0, 0.0, -3.0])
        plain = batchnorm_forward(batch, torch.ones(3), torch.zeros(3), fresh_running(3))
        scaled = batchnorm_forward(batch, gamma, beta, fresh_running(3))
        self.assertTrue(torch.allclose(scaled, plain * gamma + beta, atol=1e-6))

    def test_batch_of_one_raises_in_training_but_works_in_eval(self):
        running = {"mean": torch.tensor([0.2, 2.0]), "var": torch.tensor([1.1, 20.9])}
        single = torch.tensor([[1.0, 10.0]])
        with self.assertRaises(ValueError):
            batchnorm_forward(single, torch.ones(2), torch.zeros(2), running, 0.1, True)
        self.assertTrue(torch.equal(running["mean"], torch.tensor([0.2, 2.0])))
        self.assertTrue(torch.equal(running["var"], torch.tensor([1.1, 20.9])))
        out = batchnorm_forward(single, torch.ones(2), torch.zeros(2), running, 0.1, False)
        self.assertTrue(torch.allclose(out, torch.tensor([[0.7628, 1.7499]]), atol=1e-4))

    def test_gamma_beta_get_gradients_but_running_stats_do_not(self):
        torch.manual_seed(4)
        batch = torch.randn(5, 3, requires_grad=True)
        gamma = torch.ones(3, requires_grad=True)
        beta = torch.zeros(3, requires_grad=True)
        running = fresh_running(3)
        out = batchnorm_forward(batch, gamma, beta, running)
        (out * torch.randn(5, 3)).sum().backward()
        self.assertGreater(gamma.grad.abs().sum().item(), 0.0)
        self.assertGreater(beta.grad.abs().sum().item(), 0.0)
        self.assertFalse(running["mean"].requires_grad)
        self.assertFalse(running["var"].requires_grad)


if __name__ == "__main__":
    unittest.main(verbosity=2)
