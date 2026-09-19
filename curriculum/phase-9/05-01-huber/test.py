import unittest

import torch
import torch.nn.functional as F

from solution import huber, huber_grad


def torch_huber(y, yhat, delta):
    p = torch.tensor(yhat, dtype=torch.float64, requires_grad=True)
    loss = F.huber_loss(p, torch.tensor(y, dtype=torch.float64), delta=delta)
    loss.backward()
    return loss.item(), p.grad.tolist()


class TestHuber(unittest.TestCase):
    def test_inside_band_is_half_squared_error(self):
        self.assertAlmostEqual(huber([0.0], [0.5]), 0.125)
        self.assertAlmostEqual(huber([2.0, 1.0], [1.8, 1.3], delta=1.0), (0.5 * 0.04 + 0.5 * 0.09) / 2)

    def test_outside_band_is_shifted_l1(self):
        self.assertAlmostEqual(huber([0.0], [3.0]), 2.5)
        self.assertAlmostEqual(huber([1.0], [-3.0], delta=2.0), 6.0)

    def test_mean_reduction(self):
        self.assertAlmostEqual(huber([0.0, 0.0], [0.5, 3.0]), 1.3125)
        self.assertIsInstance(huber([0.0], [0.5]), float)

    def test_gradient_examples(self):
        for got, want in zip(huber_grad([0.0, 0.0], [0.5, 3.0]), [0.25, 0.5]):
            self.assertAlmostEqual(got, want)
        for got, want in zip(huber_grad([0.0, 0.0], [-0.5, -30.0]), [-0.25, -0.5]):
            self.assertAlmostEqual(got, want)

    def test_boundary_is_continuous(self):
        self.assertAlmostEqual(huber([0.0], [1.5], delta=1.5), 0.5 * 1.5 ** 2)
        self.assertAlmostEqual(huber_grad([0.0], [1.5], delta=1.5)[0], 1.5)

    def test_matches_pytorch_loss_and_autograd(self):
        g = torch.Generator().manual_seed(0)
        for delta in (0.5, 1.0, 2.5):
            y = (torch.randn(40, generator=g) * 3).tolist()
            yhat = (torch.randn(40, generator=g) * 3).tolist()
            want_loss, want_grad = torch_huber(y, yhat, delta)
            self.assertAlmostEqual(huber(y, yhat, delta), want_loss, delta=1e-9)
            got = huber_grad(y, yhat, delta)
            self.assertEqual(len(got), 40)
            for a, b in zip(got, want_grad):
                self.assertAlmostEqual(a, b, delta=1e-9)

    def test_outlier_pull_is_capped(self):
        small = huber_grad([0.0, 0.0], [0.0, 10.0])[1]
        huge = huber_grad([0.0, 0.0], [0.0, 1e6])[1]
        self.assertAlmostEqual(small, huge)

    def test_bad_input(self):
        for args in (([], []), ([1.0], [1.0, 2.0]), ([1.0], [1.0], 0.0), ([1.0], [1.0], -1.0)):
            with self.assertRaises(ValueError, msg=repr(args)):
                huber(*args)
            with self.assertRaises(ValueError, msg=repr(args)):
                huber_grad(*args)


if __name__ == "__main__":
    unittest.main(verbosity=2)
