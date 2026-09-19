import unittest

import torch

from solution import sgd_momentum_step


class TestSgdMomentumStep(unittest.TestCase):
    def test_first_step(self):
        params, state = [1.0, -2.0], []
        out = sgd_momentum_step(params, [0.5, -1.0], state, 0.1, 0.9)
        for got, want in zip(out, [0.5, -1.0]):
            self.assertAlmostEqual(got, want, places=12)
        for got, want in zip(params, [0.95, -1.9]):
            self.assertAlmostEqual(got, want, places=12)

    def test_second_step_uses_the_velocity(self):
        params, state = [1.0, -2.0], []
        sgd_momentum_step(params, [0.5, -1.0], state, 0.1, 0.9)
        out = sgd_momentum_step(params, [0.5, -1.0], state, 0.1, 0.9)
        for got, want in zip(out, [0.95, -1.9]):
            self.assertAlmostEqual(got, want, places=12)
        for got, want in zip(params, [0.855, -1.71]):
            self.assertAlmostEqual(got, want, places=12)

    def test_updates_in_place_and_returns_state(self):
        params, state = [1.0, 2.0], []
        out = sgd_momentum_step(params, [1.0, 1.0], state, 0.5, 0.5)
        self.assertIs(out, state)
        self.assertEqual(len(state), 2)
        self.assertAlmostEqual(params[0], 0.5, places=12)

    def test_beta_zero_is_plain_sgd(self):
        params, state = [1.0], []
        for _ in range(3):
            sgd_momentum_step(params, [2.0], state, 0.1, 0.0)
        self.assertAlmostEqual(params[0], 0.4, places=12)
        self.assertAlmostEqual(state[0], 2.0, places=12)

    def test_matches_torch_sgd_over_many_steps(self):
        # Minimise f(p) = sum(a * p^2) with gradient 2 * a * p.
        a = [1.0, 3.0, 0.5]
        start = [1.0, -2.0, 4.0]
        p_torch = torch.tensor(start, dtype=torch.float64, requires_grad=True)
        opt = torch.optim.SGD([p_torch], lr=0.05, momentum=0.8)
        params, state = list(start), []
        for _ in range(20):
            opt.zero_grad()
            (torch.tensor(a, dtype=torch.float64) * p_torch ** 2).sum().backward()
            opt.step()
            grads = [2 * ai * pi for ai, pi in zip(a, params)]
            sgd_momentum_step(params, grads, state, 0.05, 0.8)
        for got, want in zip(params, p_torch.tolist()):
            self.assertAlmostEqual(got, want, delta=1e-9)

    def test_rejects_bad_arguments_without_changes(self):
        params = [1.0, 2.0]
        for args in [([1.0], [], 0.1, 0.9), ([1.0, 1.0], [0.0], 0.1, 0.9),
                     ([1.0, 1.0], [], 0.0, 0.9), ([1.0, 1.0], [], 0.1, 1.0), ([1.0, 1.0], [], 0.1, -0.1)]:
            with self.assertRaises(ValueError, msg=str(args)):
                sgd_momentum_step(params, *args)
        self.assertEqual(params, [1.0, 2.0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
