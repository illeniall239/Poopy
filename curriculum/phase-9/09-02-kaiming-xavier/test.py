import math
import unittest

import numpy as np
import torch
from torch import nn

from solution import kaiming_std, xavier_bound


class TestKaimingXavier(unittest.TestCase):
    def test_kaiming_values(self):
        self.assertAlmostEqual(kaiming_std(512, math.sqrt(2)), 0.0625, places=12)
        self.assertAlmostEqual(kaiming_std(100, 1.0), 0.1, places=12)
        self.assertAlmostEqual(kaiming_std(9, 5 / 3), 5 / 9, places=12)
        self.assertIsInstance(kaiming_std(4, 1.0), float)

    def test_xavier_values(self):
        self.assertAlmostEqual(xavier_bound(100, 200), math.sqrt(0.02), places=12)
        self.assertAlmostEqual(xavier_bound(3, 3), 1.0, places=12)
        self.assertIsInstance(xavier_bound(1, 1), float)

    def test_kaiming_matches_torch_on_a_linear_weight(self):
        torch.manual_seed(0)
        layer = nn.Linear(400, 50)  # weight shape (50, 400): fan_in is 400, fan_out is 50
        gain = nn.init.calculate_gain("relu")
        nn.init.kaiming_normal_(layer.weight, mode="fan_in", nonlinearity="relu")
        got = kaiming_std(400, gain)
        self.assertAlmostEqual(layer.weight.std().item() / got, 1.0, delta=0.03)
        self.assertNotAlmostEqual(got, kaiming_std(50, gain), places=3)

    def test_xavier_matches_torch(self):
        torch.manual_seed(0)
        w = torch.empty(300, 100)
        nn.init.xavier_uniform_(w)
        a = xavier_bound(100, 300)
        self.assertLessEqual(w.abs().max().item(), a + 1e-7)
        self.assertGreater(w.abs().max().item(), 0.99 * a)
        self.assertAlmostEqual(w.var().item() / (a * a / 3), 1.0, delta=0.03)

    def test_kaiming_keeps_relu_activations_steady(self):
        rng = np.random.default_rng(0)
        width = 256
        x = rng.standard_normal((1000, width))
        start = np.mean(x ** 2)
        for _ in range(20):
            W = rng.standard_normal((width, width)) * kaiming_std(width, math.sqrt(2))
            x = np.maximum(0.0, x @ W)
        ratio = np.mean(x ** 2) / start
        self.assertGreater(ratio, 0.3)
        self.assertLess(ratio, 3.0)

    def test_rejects_bad_arguments(self):
        with self.assertRaises(ValueError):
            kaiming_std(0, 1.0)
        with self.assertRaises(ValueError):
            kaiming_std(10, 0.0)
        with self.assertRaises(ValueError):
            xavier_bound(0, 10)
        with self.assertRaises(ValueError):
            xavier_bound(10, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
