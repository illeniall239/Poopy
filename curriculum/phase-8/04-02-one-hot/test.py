import random
import unittest

import numpy as np

from solution import bucketize, one_hot


class TestOneHot(unittest.TestCase):
    def test_known_and_unknown(self):
        self.assertEqual(
            one_hot(["red", "blue", "green", "red"], ["blue", "red"]),
            [[0, 1, 0], [1, 0, 0], [0, 0, 1], [0, 1, 0]],
        )

    def test_column_order_follows_vocabulary_not_values(self):
        vocab = ["c", "a", "b"]
        self.assertEqual(one_hot(["a", "b", "c"], vocab), [[0, 1, 0, 0], [0, 0, 1, 0], [1, 0, 0, 0]])
        # The same vocabulary gives the same column for a value, whatever else is in the batch.
        self.assertEqual(one_hot(["b"], vocab)[0], one_hot(["c", "a", "b"], vocab)[2])

    def test_every_row_has_exactly_one_hot(self):
        rng = random.Random(0)
        vocab = [f"cat{i}" for i in range(50)]
        values = [f"cat{rng.randrange(80)}" for _ in range(2000)]
        rows = one_hot(values, vocab)
        self.assertEqual(len(rows), 2000)
        for value, row in zip(values, rows):
            self.assertEqual(len(row), 51)
            self.assertEqual(sum(row), 1)
            self.assertEqual(row.index(1), vocab.index(value) if value in vocab else 50)

    def test_edge_cases(self):
        self.assertEqual(one_hot(["Red"], ["blue", "red"]), [[0, 0, 1]])
        self.assertEqual(one_hot([], ["a"]), [])
        self.assertEqual(one_hot(["x", "y"], []), [[1], [1]])
        with self.assertRaises(ValueError):
            one_hot(["a"], ["a", "b", "a"])

    def test_bucketize_examples(self):
        b = [10, 20, 30]
        self.assertEqual(bucketize(5, b), 0)
        self.assertEqual(bucketize(25, b), 2)
        self.assertEqual(bucketize(99, b), 3)
        self.assertEqual(bucketize(-1e9, b), 0)

    def test_bucketize_boundary_goes_up(self):
        b = [10, 20, 30]
        self.assertEqual(bucketize(10, b), 1)
        self.assertEqual(bucketize(20, b), 2)
        self.assertEqual(bucketize(30, b), 3)
        self.assertEqual(bucketize(19.999, b), 1)
        self.assertEqual(bucketize(0.5, [0.5]), 1)

    def test_bucketize_matches_numpy_digitize(self):
        rng = random.Random(1)
        b = sorted(rng.sample(range(-100, 100), 12))
        for _ in range(500):
            x = rng.choice([rng.uniform(-120, 120), float(rng.choice(b))])
            self.assertEqual(bucketize(x, b), int(np.digitize(x, b, right=False)), x)

    def test_bucketize_rejects_bad_boundaries(self):
        with self.assertRaises(ValueError):
            bucketize(1, [3, 2])
        with self.assertRaises(ValueError):
            bucketize(1, [1, 2, 2, 3])
        with self.assertRaises(ValueError):
            bucketize(1, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
