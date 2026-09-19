import unittest

import torch
import torch.nn.functional as F
from torch import nn

from solution import freeze_backbone, replace_head


def make_model():
    return nn.Sequential(nn.Linear(4, 16), nn.ReLU(), nn.Linear(16, 16), nn.ReLU(), nn.Linear(16, 2))


def data(n, seed):
    """Task A: sign of x0 + x1 (2 classes). Task B: x0 + x1 cut into 3 bands (3 classes)."""
    g = torch.Generator().manual_seed(seed)
    X = torch.randn(n, 4, generator=g)
    s = X[:, 0] + X[:, 1]
    return X, (s > 0).long(), (s > -0.6).long() + (s > 0.6).long()


def train(model, X, y, steps, lr):
    opt = torch.optim.Adam(model.parameters(), lr=lr)  # deliberately over ALL parameters
    for _ in range(steps):
        opt.zero_grad()
        F.cross_entropy(model(X), y).backward()
        opt.step()


def pretrained():
    torch.manual_seed(0)
    model = make_model()
    X, y_a, _ = data(256, 100)
    train(model, X, y_a, 200, 0.01)
    return model


class TestFreezeAndHead(unittest.TestCase):
    def test_freeze_leaves_only_head_trainable(self):
        model = make_model()
        self.assertIs(freeze_backbone(model), model)
        self.assertEqual([n for n, p in model.named_parameters() if p.requires_grad], ["4.weight", "4.bias"])

    def test_freeze_reenables_a_frozen_head(self):
        model = make_model()
        for p in model.parameters():
            p.requires_grad = False
        freeze_backbone(model)
        self.assertTrue(all(p.requires_grad for p in model[-1].parameters()))

    def test_replace_head_shape_and_identity(self):
        model = make_model()
        old_backbone = model[0]
        self.assertIs(replace_head(model, 3), model)
        self.assertIsInstance(model[-1], nn.Linear)
        self.assertEqual((model[-1].in_features, model[-1].out_features), (16, 3))
        self.assertIs(model[0], old_backbone)
        self.assertEqual(len(model), 5)
        self.assertEqual(tuple(model(torch.randn(2, 4)).shape), (2, 3))

    def test_replace_after_freeze_only_new_head_trainable(self):
        model = replace_head(freeze_backbone(make_model()), 3)
        trainable = [p for p in model.parameters() if p.requires_grad]
        self.assertEqual(len(trainable), 2)
        self.assertEqual({tuple(p.shape) for p in trainable}, {(3, 16), (3,)})

    def test_training_does_not_move_the_backbone(self):
        model = replace_head(freeze_backbone(pretrained()), 3)
        before = [p.detach().clone() for p in model[:-1].parameters()]
        head_before = model[-1].weight.detach().clone()
        X, _, y_b = data(48, 200)
        train(model, X, y_b, 20, 0.05)
        for b, p in zip(before, model[:-1].parameters()):
            self.assertTrue(torch.equal(b, p))
        self.assertFalse(torch.equal(head_before, model[-1].weight))

    def test_fine_tuned_head_transfers(self):
        model = replace_head(freeze_backbone(pretrained()), 3)
        torch.manual_seed(1)
        X, _, y_b = data(48, 200)
        train(model, X, y_b, 300, 0.05)
        X_test, _, y_test = data(200, 300)
        with torch.no_grad():
            acc = (model(X_test).argmax(1) == y_test).float().mean().item()
        self.assertGreaterEqual(acc, 0.8)

    def test_errors(self):
        with self.assertRaises(ValueError):
            replace_head(nn.Sequential(nn.Linear(4, 2), nn.ReLU()), 3)
        with self.assertRaises(ValueError):
            freeze_backbone(nn.Sequential(nn.Linear(4, 2), nn.ReLU()))
        with self.assertRaises(ValueError):
            replace_head(make_model(), 0)
        with self.assertRaises(ValueError):
            freeze_backbone(nn.Linear(4, 2))


if __name__ == "__main__":
    unittest.main(verbosity=2)
