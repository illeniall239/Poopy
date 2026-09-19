import math
import unittest

import torch
import torch.nn.functional as F

from solution import CharMLP, make_dataset, train_lm

WORDS = ["emma", "olivia", "ava", "isabella", "sophia", "mia", "amelia", "ella"]


class TestCharMLP(unittest.TestCase):
    def test_dataset_by_hand(self):
        X, Y = make_dataset(["ab"], 2)
        self.assertEqual(X.dtype, torch.long)
        self.assertEqual(Y.dtype, torch.long)
        self.assertEqual(X.tolist(), [[0, 0], [0, 1], [1, 2]])
        self.assertEqual(Y.tolist(), [1, 2, 0])

    def test_dataset_size_and_context_reset(self):
        X, Y = make_dataset(["ab", "c"], 3)
        self.assertEqual(tuple(X.shape), (5, 3))
        self.assertEqual(X[3].tolist(), [0, 0, 0])  # a new word starts from an empty context
        self.assertEqual(Y.tolist(), [1, 2, 0, 3, 0])
        X, Y = make_dataset(WORDS, 3)
        self.assertEqual(len(Y), sum(len(w) + 1 for w in WORDS))
        with self.assertRaises(ValueError):
            make_dataset(["Ab"], 3)

    def test_model_shape_and_parameter_count(self):
        torch.manual_seed(0)
        model = CharMLP(27, 3, 8, 64)
        self.assertEqual(tuple(model(torch.zeros(5, 3, dtype=torch.long)).shape), (5, 27))
        self.assertEqual(sum(p.numel() for p in model.parameters()), 27 * 8 + (24 * 64 + 64) + (64 * 27 + 27))
        self.assertEqual(sum(p.numel() for p in CharMLP(10, 2, 4, 5).parameters()), 40 + 45 + 60)

    def test_positions_are_not_interchangeable(self):
        torch.manual_seed(0)
        model = CharMLP(27, 3, 8, 16)
        a = model(torch.tensor([[1, 2, 3]]))
        b = model(torch.tensor([[3, 2, 1]]))
        self.assertFalse(torch.allclose(a, b))

    def test_forward_is_embed_concat_tanh_linear(self):
        torch.manual_seed(3)
        model = CharMLP(27, 3, 4, 10)
        emb = [m for m in model.modules() if isinstance(m, torch.nn.Embedding)]
        linears = {m.in_features: m for m in model.modules() if isinstance(m, torch.nn.Linear)}
        self.assertEqual(len(emb), 1)
        self.assertEqual(set(linears), {12, 10})
        x = torch.tensor([[0, 5, 9], [26, 1, 1]])
        e = emb[0].weight[x].reshape(2, 12)
        expected = linears[10](torch.tanh(linears[12](e)))
        self.assertTrue(torch.allclose(model(x), expected, atol=1e-6))

    def test_initial_loss_is_near_uniform(self):
        X, Y = make_dataset(WORDS, 3)
        torch.manual_seed(0)
        losses = train_lm(CharMLP(27, 3, 8, 64), X, Y, 1, 0.01)
        self.assertEqual(len(losses), 1)
        self.assertIsInstance(losses[0], float)
        self.assertLess(abs(losses[0] - math.log(27)), 0.6)

    def test_training_drives_nll_below_threshold(self):
        X, Y = make_dataset(WORDS, 3)
        torch.manual_seed(0)
        model = CharMLP(27, 3, 8, 64)
        losses = train_lm(model, X, Y, 200, 0.01)
        self.assertEqual(len(losses), 200)
        self.assertLess(losses[-1], 0.6)
        self.assertLess(losses[-1], losses[0])
        with torch.no_grad():
            self.assertLess(F.cross_entropy(model(X), Y).item(), 0.6)  # the model itself was trained in place

    def test_same_seed_gives_the_same_run(self):
        X, Y = make_dataset(WORDS, 3)
        runs = []
        for _ in range(2):
            torch.manual_seed(7)
            runs.append(train_lm(CharMLP(27, 3, 8, 32), X, Y, 20, 0.01))
        self.assertEqual(runs[0], runs[1])


if __name__ == "__main__":
    unittest.main(verbosity=2)
