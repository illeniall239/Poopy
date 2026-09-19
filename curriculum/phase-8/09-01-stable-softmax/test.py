import unittest

import numpy as np
from numpy.testing import assert_allclose

from solution import softmax, top_k_accuracy

STRICT = dict(over="raise", divide="raise", invalid="raise")


def reference_softmax(z):
    e = np.exp(z - z.max(axis=-1, keepdims=True))
    return e / e.sum(axis=-1, keepdims=True)


class TestStableSoftmax(unittest.TestCase):
    def test_moderate_values(self):
        assert_allclose(softmax(np.array([1.0, 2.0, 3.0])), [0.09003057317038046, 0.24472847105479764, 0.6652409557748219], rtol=1e-12)
        assert_allclose(softmax(np.array([[0.0, 0.0], [0.0, np.log(3)]])), [[0.5, 0.5], [0.25, 0.75]], rtol=1e-12)

    def test_large_logits_do_not_overflow(self):
        with np.errstate(**STRICT):
            out = softmax(np.array([1000.0, 1001.0]))
            big = softmax(np.array([[1e5, -1e5, 0.0], [-1000.0, -1001.0, -1002.0]]))
        assert_allclose(out, [1 / (1 + np.e), np.e / (1 + np.e)], rtol=1e-12)
        assert_allclose(big[0], [1.0, 0.0, 0.0], atol=0)
        assert_allclose(big[1], softmax(np.array([0.0, -1.0, -2.0])), rtol=1e-12)

    def test_rows_sum_to_one_and_shape_kept(self):
        rng = np.random.default_rng(0)
        z = rng.normal(scale=50, size=(500, 7))
        p = softmax(z)
        self.assertEqual(p.shape, (500, 7))
        assert_allclose(p.sum(axis=1), np.ones(500), atol=1e-12)
        self.assertTrue(np.all((p >= 0) & (p <= 1)))
        assert_allclose(p, reference_softmax(z), rtol=1e-9, atol=1e-15)

    def test_shift_invariant_not_scale_invariant(self):
        z = np.array([0.5, 1.5, -2.0])
        assert_allclose(softmax(z + 123.0), softmax(z), rtol=1e-12)
        self.assertGreater(softmax(z * 3)[1], softmax(z)[1])
        self.assertLess(softmax(z / 3)[1], softmax(z)[1])

    def test_top_k_examples(self):
        logits = np.array([[0.1, 0.5, 0.4], [0.9, 0.05, 0.05]])
        self.assertEqual(top_k_accuracy(logits, np.array([2, 0]), 1), 0.5)
        self.assertEqual(top_k_accuracy(logits, np.array([2, 0]), 2), 1.0)
        self.assertEqual(top_k_accuracy(logits, np.array([2, 0]), 3), 1.0)
        self.assertIsInstance(top_k_accuracy(logits, np.array([2, 0]), 1), float)

    def test_top_k_tie_rule(self):
        self.assertEqual(top_k_accuracy(np.array([[1.0, 1.0, 0.0]]), np.array([1]), 1), 0.0)
        self.assertEqual(top_k_accuracy(np.array([[1.0, 1.0, 0.0]]), np.array([0]), 1), 1.0)
        self.assertEqual(top_k_accuracy(np.array([[1.0, 1.0, 1.0]]), np.array([2]), 2), 0.0)
        self.assertEqual(top_k_accuracy(np.array([[1.0, 1.0, 1.0]]), np.array([1]), 2), 1.0)

    def test_top_1_matches_argmax_and_random_data(self):
        rng = np.random.default_rng(1)
        z = rng.normal(size=(10_000, 10))
        t = rng.integers(0, 10, size=10_000)
        self.assertAlmostEqual(top_k_accuracy(z, t, 1), float(np.mean(z.argmax(axis=1) == t)), places=12)
        order = np.argsort(-z, axis=1, kind="stable")[:, :3]
        expected = float(np.mean(np.any(order == t[:, None], axis=1)))
        self.assertAlmostEqual(top_k_accuracy(z, t, 3), expected, places=12)
        self.assertAlmostEqual(top_k_accuracy(z * 1000, t, 3), expected, places=12)

    def test_rejects_bad_input(self):
        z = np.zeros((2, 3))
        with self.assertRaises(ValueError):
            top_k_accuracy(z, np.array([0, 1]), 0)
        with self.assertRaises(ValueError):
            top_k_accuracy(z, np.array([0, 1]), 4)
        with self.assertRaises(ValueError):
            top_k_accuracy(z, np.array([0]), 1)
        with self.assertRaises(ValueError):
            top_k_accuracy(z, np.array([0, 3]), 1)
        with self.assertRaises(ValueError):
            top_k_accuracy(np.zeros(3), np.array([0]), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
