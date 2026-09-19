import unittest

import numpy as np
import torch
from numpy.testing import assert_allclose
from torch import nn

from solution import MLP, load_weights, loss_and_grads

EXAMPLE = [([[0.5, -0.5], [0.25, 1.0]], [0.0, 0.1]), ([[1.0, -1.0]], [0.5])]


def t(x):
    return torch.tensor(x, dtype=torch.float64)


def hand_backprop(weights, X, y):
    """Plain numpy forward and backward for a tanh MLP with a raw last layer and mean squared error."""
    Ws = [np.array(W, dtype=float) for W, _ in weights]
    bs = [np.array(b, dtype=float) for _, b in weights]
    acts, h = [X], X
    for i, (W, b) in enumerate(zip(Ws, bs)):
        h = h @ W.T + b
        if i < len(Ws) - 1:
            h = np.tanh(h)
        acts.append(h)
    loss = float(np.mean((h - y) ** 2))
    d = 2 * (h - y) / h.size
    grads = []
    for i in reversed(range(len(Ws))):
        if i < len(Ws) - 1:
            d = d * (1 - acts[i + 1] ** 2)
        grads = [d.T @ acts[i], d.sum(axis=0)] + grads
        d = d @ Ws[i]
    return loss, grads


def random_weights(sizes, rng):
    return [(rng.normal(size=(o, i)).tolist(), rng.normal(size=o).tolist()) for i, o in zip(sizes, sizes[1:])]


class TestTorchMLP(unittest.TestCase):
    def test_structure(self):
        model = MLP([3, 4, 2])
        self.assertIsInstance(model.layers, nn.ModuleList)
        self.assertEqual(len(model.layers), 2)
        self.assertEqual(sum(p.numel() for p in model.parameters()), 3 * 4 + 4 + 4 * 2 + 2)
        self.assertTrue(all(p.dtype == torch.float64 for p in model.parameters()))
        with self.assertRaises(ValueError):
            MLP([3])

    def test_forward_matches_hand_computation(self):
        model = MLP([2, 2, 1])
        load_weights(model, EXAMPLE)
        out = model(t([[1.0, 2.0], [0.0, 0.0]]))
        self.assertEqual(tuple(out.shape), (2, 1))
        want = 1.0 * np.tanh(-0.5) - np.tanh(2.35) + 0.5
        want0 = np.tanh(0.0) - np.tanh(0.1) + 0.5
        assert_allclose(out.detach().numpy(), [[want], [want0]], atol=1e-12)

    def test_last_layer_has_no_tanh(self):
        model = MLP([1, 1])
        load_weights(model, [([[3.0]], [2.0])])
        self.assertAlmostEqual(model(t([[1.0]])).item(), 5.0, places=12)

    def test_load_keeps_the_same_leaf_parameters(self):
        model = MLP([2, 2, 1])
        before = [id(p) for p in model.parameters()]
        load_weights(model, EXAMPLE)
        params = list(model.parameters())
        self.assertEqual([id(p) for p in params], before)
        self.assertTrue(all(p.is_leaf and p.requires_grad for p in params))
        assert_allclose(params[0].detach().numpy(), EXAMPLE[0][0])

    def test_example_gradients(self):
        model = MLP([2, 2, 1])
        load_weights(model, EXAMPLE)
        loss, grads = loss_and_grads(model, t([[1.0, 2.0]]), t([[0.0]]))
        self.assertIsInstance(loss, float)
        self.assertAlmostEqual(loss, 0.89130699, places=7)
        assert_allclose(grads[2].numpy(), [[0.87256089, -1.85414364]], atol=1e-7)
        assert_allclose(grads[3].numpy(), [-1.88818112], atol=1e-7)
        assert_allclose(grads[1].numpy(), [-1.48495576, 0.06746138], atol=1e-7)

    def test_gradients_match_hand_backprop_on_a_batch(self):
        rng = np.random.default_rng(0)
        sizes = [3, 4, 4, 2]
        weights = random_weights(sizes, rng)
        X, y = rng.normal(size=(5, 3)), rng.normal(size=(5, 2))
        model = MLP(sizes)
        load_weights(model, weights)
        loss, grads = loss_and_grads(model, t(X), t(y))
        want_loss, want = hand_backprop(weights, X, y)
        self.assertAlmostEqual(loss, want_loss, delta=1e-10)
        self.assertEqual(len(grads), len(want))
        for g, w in zip(grads, want):
            assert_allclose(g.numpy(), w, atol=1e-10)

    def test_second_call_does_not_accumulate(self):
        rng = np.random.default_rng(1)
        model = MLP([2, 3, 1])
        load_weights(model, random_weights([2, 3, 1], rng))
        X, y = t(rng.normal(size=(4, 2))), t(rng.normal(size=(4, 1)))
        _, first = loss_and_grads(model, X, y)
        _, second = loss_and_grads(model, X, y)
        for a, b in zip(first, second):
            assert_allclose(a.numpy(), b.numpy(), atol=1e-12)

    def test_load_rejects_bad_shapes(self):
        model = MLP([2, 2, 1])
        with self.assertRaises(ValueError):
            load_weights(model, EXAMPLE[:1])
        with self.assertRaises(ValueError):
            load_weights(model, [([[0.5, -0.5, 1.0], [0.25, 1.0, 1.0]], [0.0, 0.1]), EXAMPLE[1]])
        with self.assertRaises(ValueError):
            load_weights(model, [EXAMPLE[0], ([[1.0, -1.0]], [0.5, 0.5])])


if __name__ == "__main__":
    unittest.main(verbosity=2)
