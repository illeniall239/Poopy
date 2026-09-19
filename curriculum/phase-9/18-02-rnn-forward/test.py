import math
import unittest

import torch

from solution import rnn_forward


class TestRnnForward(unittest.TestCase):
    def assertVecsAlmostEqual(self, got, want, places=6):
        self.assertEqual(len(got), len(want))
        for g_row, w_row in zip(got, want):
            self.assertEqual(len(g_row), len(w_row))
            for g, w in zip(g_row, w_row):
                self.assertAlmostEqual(g, w, places=places)

    def test_hand_trace_carries_the_hidden_state(self):
        hs = rnn_forward([[1.0], [0.0], [0.0]], [0.0], [[1.0]], [[0.5]], [0.0])
        h1 = math.tanh(1.0)
        h2 = math.tanh(0.5 * h1)
        h3 = math.tanh(0.5 * h2)
        self.assertVecsAlmostEqual(hs, [[h1], [h2], [h3]], places=12)

    def test_initial_state_matters(self):
        hs = rnn_forward([[0.0]], [2.0], [[1.0]], [[1.0]], [0.5])
        self.assertAlmostEqual(hs[0][0], math.tanh(2.5), places=12)

    def test_two_units_hand_trace(self):
        Wxh = [[1.0, 0.0], [0.0, -1.0]]
        Whh = [[0.0, 1.0], [1.0, 0.0]]
        b = [0.1, 0.0]
        hs = rnn_forward([[1.0, 2.0], [0.5, 0.5]], [0.0, 0.0], Wxh, Whh, b)
        h1 = [math.tanh(1.1), math.tanh(-2.0)]
        h2 = [math.tanh(0.5 + h1[1] + 0.1), math.tanh(-0.5 + h1[0])]
        self.assertVecsAlmostEqual(hs, [h1, h2], places=12)

    def test_empty_sequence(self):
        self.assertEqual(rnn_forward([], [0.3, -0.2], [[1.0], [2.0]], [[0.0, 0.0], [0.0, 0.0]], [0.0, 0.0]), [])

    def test_matches_torch_rnn(self):
        torch.manual_seed(0)
        T, D, H = 5, 3, 4
        rnn = torch.nn.RNN(D, H, nonlinearity="tanh", batch_first=True)
        with torch.no_grad():
            rnn.bias_hh_l0.zero_()
        x = torch.randn(1, T, D)
        h0 = torch.randn(1, 1, H)
        want, _ = rnn(x, h0)
        got = rnn_forward(
            x[0].tolist(), h0[0, 0].tolist(),
            rnn.weight_ih_l0.tolist(), rnn.weight_hh_l0.tolist(), rnn.bias_ih_l0.tolist(),
        )
        self.assertVecsAlmostEqual(got, want[0].tolist(), places=5)

    def test_rejects_mismatched_sizes(self):
        with self.assertRaises(ValueError):
            rnn_forward([[1.0, 2.0]], [0.0], [[1.0]], [[1.0]], [0.0])
        with self.assertRaises(ValueError):
            rnn_forward([[1.0]], [0.0, 0.0], [[1.0]], [[1.0]], [0.0])
        with self.assertRaises(ValueError):
            rnn_forward([[1.0]], [0.0], [[1.0]], [[1.0]], [0.0, 0.0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
