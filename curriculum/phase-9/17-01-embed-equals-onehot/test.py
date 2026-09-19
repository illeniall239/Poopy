import unittest

import torch
import torch.nn.functional as F

from solution import embed


class TestEmbedEqualsOneHot(unittest.TestCase):
    def setUp(self):
        self.table = torch.tensor([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])

    def test_picks_rows(self):
        out = embed(torch.tensor([2, 0]), self.table)
        self.assertTrue(torch.equal(out, torch.tensor([[5.0, 6.0], [1.0, 2.0]])))

    def test_equals_one_hot_matmul(self):
        torch.manual_seed(0)
        table = torch.randn(7, 4)
        idx = torch.tensor([3, 0, 6, 3, 1])
        expected = F.one_hot(idx, 7).float() @ table
        self.assertTrue(torch.allclose(embed(idx, table), expected, atol=1e-6))

    def test_keeps_the_batch_shape(self):
        torch.manual_seed(1)
        table = torch.randn(5, 3)
        idx = torch.tensor([[1, 1], [0, 4]])
        out = embed(idx, table)
        self.assertEqual(tuple(out.shape), (2, 2, 3))
        self.assertTrue(torch.allclose(out, F.one_hot(idx, 5).float() @ table, atol=1e-6))

    def test_empty_indices(self):
        out = embed(torch.tensor([], dtype=torch.long), self.table)
        self.assertEqual(tuple(out.shape), (0, 2))

    def test_rejects_out_of_range_including_negative(self):
        with self.assertRaises(ValueError):
            embed(torch.tensor([3]), self.table)
        with self.assertRaises(ValueError):
            embed(torch.tensor([0, -1]), self.table)

    def test_gradient_reaches_the_table(self):
        table = self.table.clone().requires_grad_(True)
        embed(torch.tensor([2, 0, 2]), table).sum().backward()
        self.assertIsNotNone(table.grad)
        self.assertTrue(torch.equal(table.grad, torch.tensor([[1.0, 1.0], [0.0, 0.0], [2.0, 2.0]])))

    def test_matches_nn_embedding(self):
        torch.manual_seed(2)
        layer = torch.nn.Embedding(6, 3)
        idx = torch.tensor([[5, 0, 2]])
        self.assertTrue(torch.allclose(embed(idx, layer.weight), layer(idx), atol=1e-6))


if __name__ == "__main__":
    unittest.main(verbosity=2)
