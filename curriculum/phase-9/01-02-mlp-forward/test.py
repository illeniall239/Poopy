import math
import unittest

from solution import mlp_forward

identity = lambda z: z  # noqa: E731
relu = lambda z: max(0.0, z)  # noqa: E731


class TestMlpForward(unittest.TestCase):
    def test_single_layer_hand_computed(self):
        out = mlp_forward([1.0, 2.0], [([[1.0, 1.0], [1.0, -1.0]], [0.0, 0.5], relu)])
        self.assertEqual(out, [3.0, 0.0])

    def test_two_layers_hand_computed(self):
        layers = [
            ([[1.0, 1.0], [1.0, -1.0]], [0.0, 0.5], relu),
            ([[2.0, -1.0]], [1.0], identity),
        ]
        self.assertEqual(mlp_forward([1.0, 2.0], layers), [7.0])

    def test_tanh_hidden_layer(self):
        layers = [
            ([[0.5, -0.5], [1.0, 1.0]], [0.1, -0.1], math.tanh),
            ([[1.0, 1.0]], [0.0], identity),
        ]
        expected = math.tanh(0.5 * 1.0 - 0.5 * 3.0 + 0.1) + math.tanh(1.0 + 3.0 - 0.1)
        self.assertAlmostEqual(mlp_forward([1.0, 3.0], layers)[0], expected, places=12)

    def test_no_layers_returns_the_input(self):
        self.assertEqual(mlp_forward([1.5, -2.0], []), [1.5, -2.0])

    def test_linear_layers_collapse_to_one(self):
        W1, b1 = [[1.0, 2.0], [0.0, -1.0]], [1.0, 2.0]
        W2, b2 = [[3.0, 1.0]], [-1.0]
        x = [0.5, 1.5]
        stacked = mlp_forward(x, [(W1, b1, identity), (W2, b2, identity)])
        W = [[sum(W2[0][k] * W1[k][i] for k in range(2)) for i in range(2)]]
        b = [sum(W2[0][k] * b1[k] for k in range(2)) + b2[0]]
        single = mlp_forward(x, [(W, b, identity)])
        self.assertAlmostEqual(stacked[0], single[0], places=12)

    def test_shape_mismatch_raises(self):
        with self.assertRaises(ValueError):
            mlp_forward([1.0, 2.0, 3.0], [([[1.0, 1.0]], [0.0], identity)])

    def test_output_width_follows_the_last_layer(self):
        layers = [([[1.0]] * 4, [0.0] * 4, relu), ([[1.0] * 4] * 3, [0.0] * 3, identity)]
        self.assertEqual(mlp_forward([2.0], layers), [8.0, 8.0, 8.0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
