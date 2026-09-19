import unittest

import torch
from torch import nn

from solution import BatchNorm1d


class TestBatchNormEvalInvariance(unittest.TestCase):
    def test_parameters_and_buffers(self):
        bn = BatchNorm1d(3)
        self.assertIsInstance(bn, nn.Module)
        names = sorted(name for name, _ in bn.named_parameters())
        self.assertEqual(names, ["beta", "gamma"])
        self.assertTrue(torch.equal(bn.gamma.detach(), torch.ones(3)))
        self.assertTrue(torch.equal(bn.beta.detach(), torch.zeros(3)))
        buffers = dict(bn.named_buffers())
        self.assertTrue(torch.equal(buffers["running_mean"], torch.zeros(3)))
        self.assertTrue(torch.equal(buffers["running_var"], torch.ones(3)))
        self.assertIn("running_mean", bn.state_dict())
        self.assertIn("running_var", bn.state_dict())

    def test_hand_computed_training_step(self):
        bn = BatchNorm1d(2)
        bn.train()
        out = bn(torch.tensor([[1.0, 10.0], [3.0, 30.0]]))
        self.assertTrue(torch.allclose(out, torch.tensor([[-1.0, -1.0], [1.0, 1.0]]), atol=1e-4))
        self.assertTrue(torch.allclose(bn.running_mean, torch.tensor([0.2, 2.0]), atol=1e-6))
        self.assertTrue(torch.allclose(bn.running_var, torch.tensor([1.1, 20.9]), atol=1e-5))

    def test_matches_torch_in_both_modes(self):
        torch.manual_seed(0)
        d, momentum, eps = 4, 0.25, 1e-3
        mine = BatchNorm1d(d, eps=eps, momentum=momentum)
        ref = nn.BatchNorm1d(d, eps=eps, momentum=momentum)
        with torch.no_grad():
            g, b = torch.randn(d), torch.randn(d)
            mine.gamma.copy_(g)
            mine.beta.copy_(b)
            ref.weight.copy_(g)
            ref.bias.copy_(b)
        mine.train()
        ref.train()
        for _ in range(4):
            batch = torch.randn(7, d) * 3 - 2
            self.assertTrue(torch.allclose(mine(batch), ref(batch), atol=1e-5))
        self.assertTrue(torch.allclose(mine.running_mean, ref.running_mean, atol=1e-5))
        self.assertTrue(torch.allclose(mine.running_var, ref.running_var, atol=1e-5))
        mine.eval()
        ref.eval()
        batch = torch.randn(5, d)
        self.assertTrue(torch.allclose(mine(batch), ref(batch), atol=1e-5))

    def test_eval_output_of_a_row_does_not_depend_on_its_batch(self):
        torch.manual_seed(1)
        bn = BatchNorm1d(3)
        bn.train()
        for _ in range(5):
            bn(torch.randn(8, 3) * 2 + 1)
        row = torch.randn(1, 3)
        batch_a = torch.cat([row, torch.randn(4, 3)])
        batch_b = torch.cat([torch.randn(6, 3) * 10 + 50, row])
        # Training mode: the same row gets different answers, coupled to its batch-mates.
        train_a = bn(batch_a)[0].detach().clone()
        train_b = bn(batch_b)[-1].detach().clone()
        self.assertFalse(torch.allclose(train_a, train_b, atol=1e-3))
        # Eval mode: identical, whatever the batch.
        bn.eval()
        eval_a = bn(batch_a)[0]
        eval_b = bn(batch_b)[-1]
        eval_alone = bn(row)[0]
        self.assertTrue(torch.allclose(eval_a, eval_b, atol=1e-6))
        self.assertTrue(torch.allclose(eval_a, eval_alone, atol=1e-6))

    def test_eval_leaves_running_stats_untouched(self):
        torch.manual_seed(2)
        bn = BatchNorm1d(2)
        bn.train()
        bn(torch.randn(6, 2))
        mean_before = bn.running_mean.clone()
        var_before = bn.running_var.clone()
        bn.eval()
        bn(torch.randn(6, 2) * 100)
        self.assertTrue(torch.equal(bn.running_mean, mean_before))
        self.assertTrue(torch.equal(bn.running_var, var_before))

    def test_batch_of_one_raises_in_training_but_works_in_eval(self):
        bn = BatchNorm1d(2)
        bn.train()
        bn(torch.tensor([[1.0, 10.0], [3.0, 30.0]]))
        with self.assertRaises(ValueError):
            bn(torch.tensor([[1.0, 10.0]]))
        self.assertTrue(torch.allclose(bn.running_mean, torch.tensor([0.2, 2.0]), atol=1e-6))
        bn.eval()
        out = bn(torch.tensor([[1.0, 10.0]]))
        self.assertTrue(torch.allclose(out, torch.tensor([[0.7628, 1.7499]]), atol=1e-4))

    def test_gamma_and_beta_learn_but_buffers_do_not(self):
        torch.manual_seed(3)
        bn = BatchNorm1d(3)
        bn.train()
        x = torch.randn(5, 3, requires_grad=True)
        (bn(x) * torch.randn(5, 3)).sum().backward()
        self.assertGreater(bn.gamma.grad.abs().sum().item(), 0.0)
        self.assertGreater(bn.beta.grad.abs().sum().item(), 0.0)
        self.assertFalse(bn.running_mean.requires_grad)
        self.assertFalse(bn.running_var.requires_grad)
        self.assertEqual(len(list(bn.parameters())), 2)

    def test_rejects_wrong_shapes(self):
        bn = BatchNorm1d(3)
        with self.assertRaises(ValueError):
            bn(torch.randn(4, 2))
        with self.assertRaises(ValueError):
            bn(torch.randn(4, 3, 3))


if __name__ == "__main__":
    unittest.main(verbosity=2)
