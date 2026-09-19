import unittest

import numpy as np
import torch
from numpy.testing import assert_allclose

from solution import unbroadcast

G = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])


class TestUnbroadcast(unittest.TestCase):
    def test_drops_leading_axis(self):
        out = unbroadcast(G, (3,))
        self.assertEqual(out.shape, (3,))
        assert_allclose(out, [5.0, 7.0, 9.0])

    def test_keeps_size_one_axes(self):
        a = unbroadcast(G, (1, 3))
        self.assertEqual(a.shape, (1, 3))
        assert_allclose(a, [[5.0, 7.0, 9.0]])
        b = unbroadcast(G, (2, 1))
        self.assertEqual(b.shape, (2, 1))
        assert_allclose(b, [[6.0], [15.0]])

    def test_scalar_and_same_shape(self):
        s = unbroadcast(G, ())
        self.assertEqual(np.shape(s), ())
        self.assertAlmostEqual(float(s), 21.0)
        same = unbroadcast(G, (2, 3))
        self.assertEqual(same.shape, (2, 3))
        assert_allclose(same, G)

    def test_mixed_leading_and_size_one(self):
        out = unbroadcast(np.ones((4, 2, 3)), (2, 1))
        self.assertEqual(out.shape, (2, 1))
        assert_allclose(out, [[12.0], [12.0]])
        out = unbroadcast(np.ones((2, 3, 4, 5)), (3, 1, 1))
        self.assertEqual(out.shape, (3, 1, 1))
        assert_allclose(out, np.full((3, 1, 1), 40.0))

    def test_matches_torch_autograd(self):
        rng = np.random.default_rng(0)
        big = (2, 3, 4)
        for small in [(4,), (3, 1), (1, 4), (2, 1, 4), (1, 1, 1), (3, 4), ()]:
            a = torch.tensor(rng.normal(size=small), requires_grad=True)
            b = torch.tensor(rng.normal(size=big))
            g = rng.normal(size=big)
            ((a + b) * torch.tensor(g)).sum().backward()
            out = unbroadcast(g, small)
            self.assertEqual(np.shape(out), small, msg=f"target {small}")
            assert_allclose(out, a.grad.numpy(), atol=1e-12, err_msg=f"target {small}")

    def test_does_not_modify_grad(self):
        g = G.copy()
        unbroadcast(g, (1, 3))
        assert_allclose(g, G)

    def test_rejects_shapes_that_do_not_broadcast(self):
        for bad in [(2,), (3, 3), (1, 2, 3, 1), (4, 2, 3)]:
            with self.assertRaises(ValueError, msg=f"shape {bad}"):
                unbroadcast(G, bad)


if __name__ == "__main__":
    unittest.main(verbosity=2)
