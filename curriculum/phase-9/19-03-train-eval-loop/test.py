import unittest

import torch
import torch.nn as nn
import torch.nn.functional as F

from solution import train_and_eval


class Probe(nn.Module):
    """Identity layer that records (grad enabled, training mode) at every forward pass."""

    def __init__(self):
        super().__init__()
        self.calls = []

    def forward(self, x):
        self.calls.append((torch.is_grad_enabled(), self.training, x.shape[0]))
        return x


def tiny_cnn(dropout=0.5):
    probe = Probe()
    model = nn.Sequential(
        nn.Conv2d(1, 4, 3, padding=1), nn.BatchNorm2d(4), nn.ReLU(), nn.MaxPool2d(2),
        nn.Dropout(dropout), probe, nn.Flatten(), nn.Linear(4 * 4 * 4, 2),
    )
    return model, probe


def images(n, seed):
    g = torch.Generator().manual_seed(seed)
    y = torch.randint(0, 2, (n,), generator=g)
    X = 0.3 * torch.randn(n, 1, 8, 8, generator=g)
    X[y == 0, :, :4, :] += 1.0  # class 0: bright top half
    X[y == 1, :, 4:, :] += 1.0  # class 1: bright bottom half
    return X, y


def batches(X, y, sizes):
    return list(zip(X.split(sizes), y.split(sizes)))


def data():
    Xt, yt = images(64, 0)
    Xv, yv = images(32, 1)
    return batches(Xt, yt, [16, 16, 16, 16]), batches(Xv, yv, [20, 12])


def adam(params):
    return torch.optim.Adam(params, lr=0.01)


class TestTrainEvalLoop(unittest.TestCase):
    def test_returns_one_float_per_epoch(self):
        torch.manual_seed(0)
        model, _ = tiny_cnn()
        train, val = data()
        hist = train_and_eval(model, train, val, 3, adam)
        self.assertEqual(set(hist), {"train", "val"})
        self.assertEqual((len(hist["train"]), len(hist["val"])), (3, 3))
        self.assertTrue(all(isinstance(v, float) for v in hist["train"] + hist["val"]))

    def test_learns_the_synthetic_task(self):
        torch.manual_seed(0)
        model, _ = tiny_cnn()
        train, val = data()
        hist = train_and_eval(model, train, val, 8, adam)
        self.assertLess(hist["val"][-1], hist["val"][0])
        self.assertLess(hist["val"][-1], 0.4)
        self.assertLess(hist["train"][-1], hist["train"][0])

    def test_val_runs_in_eval_mode_under_no_grad(self):
        torch.manual_seed(0)
        model, probe = tiny_cnn()
        train, val = data()
        train_and_eval(model, train, val, 2, adam)
        val_calls = [c for c in probe.calls if c[2] in (20, 12)]
        train_calls = [c for c in probe.calls if c[2] == 16]
        self.assertEqual(len(val_calls), 4)
        self.assertEqual(len(train_calls), 8)
        for grad_on, training, _ in val_calls:
            self.assertFalse(grad_on, "validation must run under torch.no_grad()")
            self.assertFalse(training, "validation must run in eval mode")
        for grad_on, training, _ in train_calls:
            self.assertTrue(grad_on)
            self.assertTrue(training, "every epoch must switch back to train mode")

    def test_val_loss_is_example_weighted_eval_loss(self):
        torch.manual_seed(0)
        model, _ = tiny_cnn()
        train, val = data()
        hist = train_and_eval(model, train, val, 2, adam)
        model.eval()
        with torch.no_grad():
            X = torch.cat([b[0] for b in val])
            y = torch.cat([b[1] for b in val])
            expected = F.cross_entropy(model(X), y).item()
        self.assertAlmostEqual(hist["val"][-1], expected, places=5)

    def test_train_loss_is_the_mean_over_the_epoch(self):
        torch.manual_seed(0)
        model, _ = tiny_cnn(dropout=0.0)
        Xt, yt = images(40, 2)
        train = batches(Xt, yt, [25, 15])
        _, val = data()
        hist = train_and_eval(model, train, val, 2, lambda p: torch.optim.SGD(p, lr=0.0))
        model.train()
        with torch.no_grad():
            expected = sum(F.cross_entropy(model(X), y).item() * len(y) for X, y in train) / 40
        self.assertAlmostEqual(hist["train"][0], expected, places=5)
        self.assertAlmostEqual(hist["train"][1], expected, places=5)

    def test_optimizer_is_made_once(self):
        calls = []

        def make(params):
            calls.append(1)
            return torch.optim.SGD(params, lr=0.1)

        torch.manual_seed(0)
        model, _ = tiny_cnn()
        train, val = data()
        train_and_eval(model, train, val, 3, make)
        self.assertEqual(len(calls), 1)

    def test_rejects_empty_input(self):
        model, _ = tiny_cnn()
        train, val = data()
        with self.assertRaises(ValueError):
            train_and_eval(model, train, val, 0, adam)
        with self.assertRaises(ValueError):
            train_and_eval(model, [], val, 1, adam)
        with self.assertRaises(ValueError):
            train_and_eval(model, train, [], 1, adam)


if __name__ == "__main__":
    unittest.main(verbosity=2)
