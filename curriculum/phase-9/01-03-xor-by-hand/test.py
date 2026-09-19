import math
import unittest

from solution import xor_net, predict


class TestXorByHand(unittest.TestCase):
    def test_net_has_the_2_2_1_shape(self):
        W1, b1, W2, b2 = xor_net()
        self.assertEqual((len(W1), len(W1[0]), len(W1[1])), (2, 2, 2))
        self.assertEqual(len(b1), 2)
        self.assertEqual((len(W2), len(W2[0])), (1, 2))
        self.assertEqual(len(b2), 1)

    def test_weights_are_finite(self):
        W1, b1, W2, b2 = xor_net()
        for v in [*W1[0], *W1[1], *b1, *W2[0], *b2]:
            self.assertTrue(math.isfinite(v))

    def test_all_four_xor_cases(self):
        net = xor_net()
        for x, want in [([0, 0], 0), ([0, 1], 1), ([1, 0], 1), ([1, 1], 0)]:
            self.assertEqual(predict(x, net), want, msg=f"input {x}")

    def test_predict_runs_a_known_net(self):
        net = ([[1.0, 1.0], [1.0, 1.0]], [0.0, -1.0], [[1.0, -2.0]], [0.0])
        self.assertEqual([predict(x, net) for x in ([0, 0], [0, 1], [1, 0], [1, 1])], [0, 1, 1, 0])

    def test_predict_uses_relu_in_the_hidden_layer(self):
        # Hidden pre-activation is -3; without ReLU the output would be 3 > 0.5.
        net = ([[-3.0, 0.0], [0.0, 0.0]], [0.0, 0.0], [[-1.0, 0.0]], [0.0])
        self.assertEqual(predict([1, 0], net), 0)

    def test_predict_thresholds_at_half(self):
        net = ([[1.0, 0.0], [0.0, 1.0]], [0.0, 0.0], [[0.4, 0.4]], [0.0])
        self.assertEqual(predict([1, 0], net), 0)
        self.assertEqual(predict([1, 1], net), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
