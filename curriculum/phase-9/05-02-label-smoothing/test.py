import unittest

import torch
import torch.nn.functional as F

from solution import label_smoothed_targets


class TestLabelSmoothing(unittest.TestCase):
    def assertListClose(self, got, want):
        self.assertEqual(len(got), len(want))
        for a, b in zip(got, want):
            self.assertAlmostEqual(a, b, places=12)

    def test_no_smoothing_is_one_hot(self):
        self.assertListClose(label_smoothed_targets(4, 2, 0.0), [0.0, 0.0, 1.0, 0.0])

    def test_examples(self):
        self.assertListClose(label_smoothed_targets(4, 2, 0.1), [0.025, 0.025, 0.925, 0.025])
        self.assertListClose(label_smoothed_targets(2, 0, 0.2), [0.9, 0.1])

    def test_sums_to_one_and_keeps_argmax(self):
        for k, t, eps in [(10, 7, 0.1), (3, 0, 0.9), (1000, 999, 0.5), (5, 2, 0.999)]:
            p = label_smoothed_targets(k, t, eps)
            self.assertEqual(len(p), k)
            self.assertAlmostEqual(sum(p), 1.0, places=12)
            self.assertEqual(max(range(k), key=p.__getitem__), t)
            self.assertTrue(all(p[t] > p[j] for j in range(k) if j != t))

    def test_uses_eps_over_k_not_k_minus_one(self):
        p = label_smoothed_targets(5, 1, 0.5)
        self.assertAlmostEqual(p[0], 0.1)
        self.assertAlmostEqual(p[1], 0.6)

    def test_matches_pytorch_label_smoothing(self):
        torch.manual_seed(0)
        logits = torch.randn(6, 5, dtype=torch.float64)
        targets = [0, 4, 2, 2, 1, 3]
        for eps in (0.0, 0.1, 0.3):
            soft = torch.tensor([label_smoothed_targets(5, t, eps) for t in targets], dtype=torch.float64)
            ours = -(soft * F.log_softmax(logits, dim=1)).sum(dim=1).mean()
            theirs = F.cross_entropy(logits, torch.tensor(targets), label_smoothing=eps)
            self.assertAlmostEqual(ours.item(), theirs.item(), places=10)

    def test_bad_input(self):
        for args in [(1, 0, 0.1), (3, 3, 0.1), (3, -1, 0.1), (3, 0, 1.0), (3, 0, -0.1), (3, 0, 1.5)]:
            with self.assertRaises(ValueError, msg=repr(args)):
                label_smoothed_targets(*args)


if __name__ == "__main__":
    unittest.main(verbosity=2)
