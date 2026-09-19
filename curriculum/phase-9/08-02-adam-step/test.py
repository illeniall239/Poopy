import unittest

import torch

from solution import adam_step

B1, B2, EPS = 0.9, 0.999, 1e-8


def torch_adam_sequence(start, grad_fn, steps, lr, b1, b2, eps):
    p = torch.tensor(start, dtype=torch.float64, requires_grad=True)
    opt = torch.optim.Adam([p], lr=lr, betas=(b1, b2), eps=eps)
    history = []
    for _ in range(steps):
        opt.zero_grad()
        p.grad = torch.tensor(grad_fn(p.tolist()), dtype=torch.float64)
        opt.step()
        history.append(p.tolist())
    return history


class TestAdamStep(unittest.TestCase):
    def test_first_step_moves_by_lr(self):
        params, state = [1.0, -1.0], {}
        out = adam_step(params, [0.2, -3.0], state, 0.1, B1, B2, EPS, 1)
        self.assertIs(out, params)
        self.assertAlmostEqual(params[0], 0.9, delta=1e-7)
        self.assertAlmostEqual(params[1], -0.9, delta=1e-7)

    def test_state_holds_raw_moments(self):
        state = {}
        adam_step([1.0, -1.0], [0.2, -3.0], state, 0.1, B1, B2, EPS, 1)
        self.assertAlmostEqual(state["m"][0], 0.02, places=12)
        self.assertAlmostEqual(state["m"][1], -0.3, places=12)
        self.assertAlmostEqual(state["v"][0], 4e-05, places=15)
        self.assertAlmostEqual(state["v"][1], 0.009, places=12)

    def test_zero_gradient_does_not_move(self):
        params = [5.0]
        adam_step(params, [0.0], {}, 0.1, B1, B2, EPS, 1)
        self.assertEqual(params, [5.0])

    def test_matches_torch_adam_sequence(self):
        grad_fn = lambda p: [2 * p[0], 6 * p[1] + 1.0, 0.5 * p[2] ** 3]
        start = [1.0, -2.0, 1.5]
        want = torch_adam_sequence(start, grad_fn, 15, 0.05, B1, B2, EPS)
        params, state = list(start), {}
        for t in range(1, 16):
            adam_step(params, grad_fn(params), state, 0.05, B1, B2, EPS, t)
            for got, w in zip(params, want[t - 1]):
                self.assertAlmostEqual(got, w, delta=1e-9, msg=f"step {t}")

    def test_matches_torch_with_other_betas_and_eps(self):
        grad_fn = lambda p: [p[0] - 3.0, -0.01]
        want = torch_adam_sequence([0.0, 0.0], grad_fn, 8, 0.3, 0.5, 0.9, 1e-3)
        params, state = [0.0, 0.0], {}
        for t in range(1, 9):
            adam_step(params, grad_fn(params), state, 0.3, 0.5, 0.9, 1e-3, t)
        for got, w in zip(params, want[-1]):
            self.assertAlmostEqual(got, w, delta=1e-9)

    def test_rejects_bad_arguments_without_changes(self):
        params = [1.0, 2.0]
        cases = [
            ([1.0], {}, 0.1, B1, B2, EPS, 1),
            ([1.0, 1.0], {}, 0.1, B1, B2, EPS, 0),
            ([1.0, 1.0], {}, 0.1, 1.0, B2, EPS, 1),
            ([1.0, 1.0], {}, 0.1, B1, 1.0, EPS, 1),
            ([1.0, 1.0], {}, 0.0, B1, B2, EPS, 1),
            ([1.0, 1.0], {}, 0.1, B1, B2, 0.0, 1),
            ([1.0, 1.0], {"m": [0.0], "v": [0.0]}, 0.1, B1, B2, EPS, 2),
        ]
        for args in cases:
            with self.assertRaises(ValueError, msg=str(args)):
                adam_step(params, *args)
        self.assertEqual(params, [1.0, 2.0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
