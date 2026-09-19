import unittest

import torch

from solution import grad_accum_schedule


class TestGradAccumSchedule(unittest.TestCase):
    def test_even_split(self):
        step_at, scale = grad_accum_schedule(8, 4)
        self.assertEqual(step_at, [3, 7])
        self.assertAlmostEqual(scale, 0.25)

    def test_leftover_group_still_steps_once(self):
        self.assertEqual(grad_accum_schedule(10, 4)[0], [3, 7, 9])
        self.assertEqual(grad_accum_schedule(9, 3)[0], [2, 5, 8])

    def test_accum_one_is_ordinary_training(self):
        step_at, scale = grad_accum_schedule(3, 1)
        self.assertEqual(step_at, [0, 1, 2])
        self.assertEqual(scale, 1.0)
        self.assertIsInstance(scale, float)

    def test_accum_larger_than_epoch(self):
        step_at, scale = grad_accum_schedule(2, 5)
        self.assertEqual(step_at, [1])
        self.assertAlmostEqual(scale, 0.2)

    def test_rejects_bad_arguments(self):
        for args in ((0, 4), (4, 0), (-1, 2), (3, -2)):
            with self.assertRaises(ValueError):
                grad_accum_schedule(*args)

    def test_scaled_accumulated_grad_equals_full_batch_grad(self):
        torch.manual_seed(0)
        X, y = torch.randn(16, 3), torch.randn(16)
        w = torch.randn(3, requires_grad=True)

        ((X @ w - y) ** 2).mean().backward()
        full = w.grad.clone()
        w.grad = None

        step_at, scale = grad_accum_schedule(4, 4)
        self.assertEqual(step_at, [3])
        for Xm, ym in zip(X.split(4), y.split(4)):
            (((Xm @ w - ym) ** 2).mean() * scale).backward()
        self.assertTrue(torch.allclose(w.grad, full, atol=1e-6))


if __name__ == "__main__":
    unittest.main(verbosity=2)
