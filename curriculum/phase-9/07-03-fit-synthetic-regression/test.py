import unittest

import torch
from torch import nn

from solution import fit


def make_data(n=200):
    g = torch.Generator().manual_seed(0)
    X = torch.rand(n, 2, generator=g) * 2 - 1
    y = (torch.sin(2 * X[:, 0]) + 0.5 * X[:, 1] ** 2).unsqueeze(1)
    return X, y


class TestFit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.X, cls.y = make_data()
        cls.model, cls.mse = fit(cls.X, cls.y, 500, 0.1)

    def test_reaches_the_threshold(self):
        self.assertIsInstance(self.mse, float)
        self.assertLess(self.mse, 0.02)

    def test_model_has_the_required_architecture(self):
        kinds = [type(m) for m in self.model]
        self.assertEqual(kinds, [nn.Linear, nn.ReLU, nn.Dropout, nn.Linear])
        self.assertEqual((self.model[0].in_features, self.model[0].out_features), (2, 32))
        self.assertAlmostEqual(self.model[2].p, 0.1)

    def test_model_is_returned_in_eval_mode(self):
        self.assertFalse(self.model.training)
        self.assertTrue(all(not m.training for m in self.model.modules()))

    def test_score_is_the_eval_mode_mse(self):
        with torch.no_grad():
            want = nn.MSELoss()(self.model(self.X), self.y).item()
        self.assertAlmostEqual(self.mse, want, delta=1e-6)

    def test_training_improves_on_the_untrained_model(self):
        _, untrained = fit(self.X, self.y, 0, 0.1)
        self.assertGreater(untrained, 0.3)
        self.assertLess(self.mse, untrained / 10)

    def test_is_reproducible(self):
        _, again = fit(self.X, self.y, 100, 0.1)
        _, again2 = fit(self.X, self.y, 100, 0.1)
        self.assertEqual(again, again2)

    def test_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            fit(self.X, self.y, -1, 0.1)
        with self.assertRaises(ValueError):
            fit(self.X, self.y[:, 0], 10, 0.1)
        with self.assertRaises(ValueError):
            fit(self.X[:, 0], self.y, 10, 0.1)
        with self.assertRaises(ValueError):
            fit(self.X, self.y[:-1], 10, 0.1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
