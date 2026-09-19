import unittest

import torch
from torch import nn

from solution import TinyCNN, train_tiny_cnn


def bars_vs_stripes(n, seed):
    """Half vertical bars (label 0), half horizontal stripes (label 1), plus noise."""
    g = torch.Generator().manual_seed(seed)
    X = torch.zeros(n, 1, 8, 8)
    y = torch.arange(n) % 2
    for i in range(n):
        lines = torch.randperm(8, generator=g)[: 1 + i % 3]
        if y[i] == 0:
            X[i, 0, :, lines] = 1.0
        else:
            X[i, 0, lines, :] = 1.0
    X += 0.2 * torch.randn(X.shape, generator=g)
    return X, y


class TestTinyCNN(unittest.TestCase):
    def setUp(self):
        torch.manual_seed(0)
        self.model = TinyCNN()

    def test_layers_are_the_specified_ones(self):
        m = self.model
        self.assertIsInstance(m.conv1, nn.Conv2d)
        self.assertEqual((m.conv1.in_channels, m.conv1.out_channels, m.conv1.kernel_size, m.conv1.padding), (1, 4, (3, 3), (1, 1)))
        self.assertIsInstance(m.pool1, nn.MaxPool2d)
        self.assertEqual((m.conv2.in_channels, m.conv2.out_channels, m.conv2.kernel_size, m.conv2.padding), (4, 8, (3, 3), (1, 1)))
        self.assertIsInstance(m.pool2, nn.MaxPool2d)
        self.assertEqual((m.fc.in_features, m.fc.out_features), (32, 2))

    def test_shapes_layer_by_layer(self):
        m, x = self.model, torch.randn(3, 1, 8, 8)
        h = m.conv1(x)
        self.assertEqual(tuple(h.shape), (3, 4, 8, 8))
        h = m.pool1(torch.relu(h))
        self.assertEqual(tuple(h.shape), (3, 4, 4, 4))
        h = m.conv2(h)
        self.assertEqual(tuple(h.shape), (3, 8, 4, 4))
        h = m.pool2(torch.relu(h))
        self.assertEqual(tuple(h.shape), (3, 8, 2, 2))
        self.assertEqual(tuple(m(x).shape), (3, 2))

    def test_parameter_count(self):
        self.assertEqual(sum(p.numel() for p in self.model.parameters()), 402)

    def test_forward_is_the_specified_composition(self):
        m, x = self.model, torch.randn(4, 1, 8, 8)
        h = m.pool2(torch.relu(m.conv2(m.pool1(torch.relu(m.conv1(x))))))
        want = m.fc(h.flatten(1))
        self.assertTrue(torch.allclose(m(x), want, atol=1e-6))

    def test_train_returns_one_float_loss_per_step(self):
        X, y = bars_vs_stripes(16, seed=1)
        losses = train_tiny_cnn(self.model, X, y, steps=5, lr=0.01)
        self.assertEqual(len(losses), 5)
        self.assertTrue(all(isinstance(v, float) for v in losses))

    def test_first_loss_is_before_any_update(self):
        X, y = bars_vs_stripes(16, seed=2)
        with torch.no_grad():
            initial = nn.CrossEntropyLoss()(self.model(X), y).item()
        losses = train_tiny_cnn(self.model, X, y, steps=3, lr=0.01)
        self.assertAlmostEqual(losses[0], initial, places=5)
        with torch.no_grad():
            after = nn.CrossEntropyLoss()(self.model(X), y).item()
        self.assertNotAlmostEqual(after, initial, places=5)

    def test_fits_bars_vs_stripes(self):
        X, y = bars_vs_stripes(64, seed=3)
        X_new, y_new = bars_vs_stripes(64, seed=4)
        losses = train_tiny_cnn(self.model, X, y, steps=150, lr=0.01)
        self.assertLess(losses[-1], losses[0])
        self.model.eval()
        with torch.no_grad():
            train_acc = (self.model(X).argmax(1) == y).float().mean().item()
            new_acc = (self.model(X_new).argmax(1) == y_new).float().mean().item()
        self.assertGreaterEqual(train_acc, 0.95)
        self.assertGreaterEqual(new_acc, 0.95)


if __name__ == "__main__":
    unittest.main(verbosity=2)
