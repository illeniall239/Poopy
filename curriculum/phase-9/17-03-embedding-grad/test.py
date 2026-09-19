import unittest

import numpy as np
import torch
from numpy.testing import assert_allclose

from solution import embedding_grad


class TestEmbeddingGrad(unittest.TestCase):
    def test_distinct_indices(self):
        g = embedding_grad(np.array([0, 2]), np.array([[1.0, 1.0], [2.0, 3.0]]), 3, 2)
        assert_allclose(g, [[1.0, 1.0], [0.0, 0.0], [2.0, 3.0]])

    def test_repeated_index_sums(self):
        g = embedding_grad(np.array([1, 1, 1]), np.array([[1.0, 0.0], [2.0, 0.0], [3.0, 5.0]]), 2, 2)
        assert_allclose(g, [[0.0, 0.0], [6.0, 5.0]])

    def test_two_dimensional_indices(self):
        g = embedding_grad(np.array([[0, 1], [1, 0]]), np.ones((2, 2, 4)), 2, 4)
        self.assertEqual(g.shape, (2, 4))
        assert_allclose(g, np.full((2, 4), 2.0))

    def test_unused_rows_are_zero(self):
        g = embedding_grad(np.array([3]), np.array([[1.0, -1.0]]), 5, 2)
        self.assertEqual(g.shape, (5, 2))
        assert_allclose(g[[0, 1, 2, 4]], np.zeros((4, 2)))

    def test_matches_torch_autograd(self):
        torch.manual_seed(0)
        emb = torch.nn.Embedding(6, 3)
        idx = torch.tensor([[1, 4, 1], [0, 1, 5]])
        out = emb(idx)
        dout = torch.randn(out.shape)
        out.backward(dout)
        g = embedding_grad(idx.numpy(), dout.numpy().astype(float), 6, 3)
        assert_allclose(g, emb.weight.grad.numpy(), atol=1e-6)

    def test_rejects_bad_shapes_and_indices(self):
        with self.assertRaises(ValueError):
            embedding_grad(np.array([0, 1]), np.ones((3, 2)), 3, 2)
        with self.assertRaises(ValueError):
            embedding_grad(np.array([0, 1]), np.ones((2, 3)), 3, 2)
        with self.assertRaises(ValueError):
            embedding_grad(np.array([0, 3]), np.ones((2, 2)), 3, 2)
        with self.assertRaises(ValueError):
            embedding_grad(np.array([-1]), np.ones((1, 2)), 3, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
