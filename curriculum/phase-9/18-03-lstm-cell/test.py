import math
import unittest

import torch

from solution import lstm_cell


def params_of(cell):
    return {"W_ih": cell.weight_ih, "W_hh": cell.weight_hh, "b_ih": cell.bias_ih, "b_hh": cell.bias_hh}


def zero_params(D, H):
    return {"W_ih": torch.zeros(4 * H, D), "W_hh": torch.zeros(4 * H, H), "b_ih": torch.zeros(4 * H), "b_hh": torch.zeros(4 * H)}


class TestLstmCell(unittest.TestCase):
    def test_zero_weights_by_hand(self):
        h_new, c_new = lstm_cell(torch.tensor([[3.0]]), torch.tensor([[0.0]]), torch.tensor([[2.0]]), zero_params(1, 1))
        self.assertAlmostEqual(c_new.item(), 1.0, places=6)
        self.assertAlmostEqual(h_new.item(), 0.5 * math.tanh(1.0), places=6)

    def test_matches_torch_lstm_cell(self):
        torch.manual_seed(0)
        B, D, H = 3, 4, 5
        cell = torch.nn.LSTMCell(D, H)
        x, h, c = torch.randn(B, D), torch.randn(B, H), torch.randn(B, H)
        want_h, want_c = cell(x, (h, c))
        got_h, got_c = lstm_cell(x, h, c, params_of(cell))
        self.assertEqual(tuple(got_h.shape), (B, H))
        self.assertTrue(torch.allclose(got_h, want_h, atol=1e-5))
        self.assertTrue(torch.allclose(got_c, want_c, atol=1e-5))

    def test_gate_order_is_i_f_g_o(self):
        # Only the forget-gate block is open; the input gate is shut: c passes through unchanged.
        H = 2
        p = zero_params(1, H)
        p["b_ih"][0:H] = -100.0   # i
        p["b_ih"][H:2 * H] = 100.0  # f
        p["b_ih"][3 * H:] = 100.0   # o
        c = torch.tensor([[0.7, -1.3]])
        h_new, c_new = lstm_cell(torch.tensor([[5.0]]), torch.zeros(1, H), c, p)
        self.assertTrue(torch.allclose(c_new, c, atol=1e-6))
        self.assertTrue(torch.allclose(h_new, torch.tanh(c), atol=1e-6))

    def test_hidden_and_cell_state_differ(self):
        torch.manual_seed(1)
        cell = torch.nn.LSTMCell(2, 3)
        h_new, c_new = lstm_cell(torch.randn(2, 2), torch.randn(2, 3), torch.randn(2, 3), params_of(cell))
        self.assertFalse(torch.allclose(h_new, c_new, atol=1e-3))
        self.assertTrue(torch.all(h_new.abs() < 1.0))

    def test_unrolled_sequence_matches_torch(self):
        torch.manual_seed(2)
        D, H = 3, 4
        cell = torch.nn.LSTMCell(D, H)
        xs = torch.randn(6, 2, D)
        h = c = torch.zeros(2, H)
        th, tc = h, c
        for x in xs:
            h, c = lstm_cell(x, h, c, params_of(cell))
            th, tc = cell(x, (th, tc))
        self.assertTrue(torch.allclose(h, th, atol=1e-5))
        self.assertTrue(torch.allclose(c, tc, atol=1e-5))

    def test_gradients_match_torch(self):
        torch.manual_seed(3)
        cell = torch.nn.LSTMCell(3, 2)
        x, h, c = torch.randn(4, 3), torch.randn(4, 2), torch.randn(4, 2)
        mine = {k: v.detach().clone().requires_grad_(True) for k, v in params_of(cell).items()}
        h_new, c_new = lstm_cell(x, h, c, mine)
        (h_new.sum() + 2 * c_new.sum()).backward()
        th, tc = cell(x, (h, c))
        (th.sum() + 2 * tc.sum()).backward()
        for k, v in params_of(cell).items():
            self.assertIsNotNone(mine[k].grad, msg=k)
            self.assertTrue(torch.allclose(mine[k].grad, v.grad, atol=1e-5), msg=k)


if __name__ == "__main__":
    unittest.main(verbosity=2)
