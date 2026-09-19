import math
import random
import unittest

from solution import MLP, Layer, Neuron, Value, train

XS = [[2.0, 3.0, -1.0], [3.0, -1.0, 0.5], [0.5, 1.0, 1.0], [1.0, 1.0, -1.0]]
YS = [1.0, -1.0, -1.0, 1.0]


def sse(model, xs, ys):
    return sum(((model(x) - y) ** 2 for x, y in zip(xs, ys)), Value(0.0))


class TestMicrogradMLP(unittest.TestCase):
    def test_parameter_count(self):
        self.assertEqual(len(MLP(3, [4, 4, 1]).parameters()), 41)
        self.assertEqual(len(MLP(2, [3, 2]).parameters()), 17)
        self.assertEqual(len(Neuron(5, random.Random(0)).parameters()), 6)
        self.assertEqual(len(Layer(2, 3, random.Random(0)).parameters()), 9)

    def test_seeded_init_order(self):
        rng = random.Random(7)
        expected = [rng.uniform(-1, 1) for _ in range(41)]
        got = [p.data for p in MLP(3, [4, 4, 1], seed=7).parameters()]
        for g, e in zip(got, expected):
            self.assertAlmostEqual(g, e, places=12)
        self.assertNotEqual([p.data for p in MLP(3, [4, 4, 1], seed=8).parameters()], got)

    def test_output_types_and_range(self):
        out = MLP(3, [4, 4, 1])([2.0, 3.0, -1.0])
        self.assertIsInstance(out, Value)
        self.assertTrue(-1.0 < out.data < 1.0)
        outs = MLP(2, [3, 2])([1.0, -1.0])
        self.assertEqual(len(outs), 2)
        self.assertTrue(all(isinstance(o, Value) for o in outs))
        self.assertEqual(len(Layer(2, 1, random.Random(0))([1.0, 2.0])), 1)

    def test_neuron_forward(self):
        n = Neuron(2, random.Random(3))
        w0, w1, b = (p.data for p in n.parameters())
        self.assertAlmostEqual(n([0.5, -2.0]).data, math.tanh(w0 * 0.5 + w1 * -2.0 + b), places=12)

    def test_loss_gradients_match_numeric(self):
        model = MLP(3, [3, 2, 1], seed=1)
        xs, ys = XS[:2], YS[:2]
        model.zero_grad()
        sse(model, xs, ys).backward()
        h = 1e-6
        for i, p in enumerate(model.parameters()):
            old = p.data
            p.data = old + h
            up = sse(model, xs, ys).data
            p.data = old - h
            down = sse(model, xs, ys).data
            p.data = old
            self.assertAlmostEqual(p.grad, (up - down) / (2 * h), delta=1e-6, msg=f"param {i}")

    def test_zero_grad(self):
        model = MLP(2, [2, 1])
        for p in model.parameters():
            p.grad = 123.0
        model.zero_grad()
        self.assertTrue(all(p.grad == 0.0 for p in model.parameters()))

    def test_train_zeroes_grads_before_backward(self):
        clean, dirty = MLP(3, [4, 4, 1], seed=0), MLP(3, [4, 4, 1], seed=0)
        for p in dirty.parameters():
            p.grad = 1000.0  # stale gradients must not leak into the update
        train(clean, XS, YS, 2, 0.05)
        train(dirty, XS, YS, 2, 0.05)
        for a, b in zip(clean.parameters(), dirty.parameters()):
            self.assertAlmostEqual(a.data, b.data, places=12)

    def test_first_step_is_one_gradient_step(self):
        model, probe = MLP(3, [4, 4, 1], seed=0), MLP(3, [4, 4, 1], seed=0)
        loss = sse(probe, XS, YS)
        loss.backward()
        losses = train(model, XS, YS, 1, 0.1)
        self.assertEqual(len(losses), 1)
        self.assertAlmostEqual(losses[0], loss.data, places=12)
        for p, q in zip(model.parameters(), probe.parameters()):
            self.assertAlmostEqual(p.data, q.data - 0.1 * q.grad, places=12)

    def test_training_drives_loss_down(self):
        losses = train(MLP(3, [4, 4, 1], seed=0), XS, YS, 100, 0.05)
        self.assertEqual(len(losses), 100)
        self.assertTrue(all(isinstance(v, float) for v in losses))
        self.assertAlmostEqual(losses[0], 7.7298, places=3)
        self.assertLess(losses[-1], 0.02)


if __name__ == "__main__":
    unittest.main(verbosity=2)
