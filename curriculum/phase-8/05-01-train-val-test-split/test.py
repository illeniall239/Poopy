import random
import unittest

from solution import train_val_test_split


class TestTrainValTestSplit(unittest.TestCase):
    def test_sizes(self):
        train, val, test = train_val_test_split(10, (0.6, 0.2, 0.2), seed=0)
        self.assertEqual((len(train), len(val), len(test)), (6, 2, 2))
        train, val, test = train_val_test_split(7, (0.5, 0.25, 0.25), 1)
        self.assertEqual((len(train), len(val), len(test)), (4, 1, 2))

    def test_disjoint_and_complete(self):
        for n, fracs in [(10, (0.6, 0.2, 0.2)), (1001, (0.7, 0.15, 0.15)), (3, (1 / 3, 1 / 3, 1 / 3)), (50, (0.8, 0.0, 0.2))]:
            train, val, test = train_val_test_split(n, fracs, seed=5)
            self.assertEqual(sorted(train + val + test), list(range(n)), (n, fracs))
            self.assertFalse(set(train) & set(val) or set(train) & set(test) or set(val) & set(test))

    def test_sizes_always_sum_to_n(self):
        rng = random.Random(0)
        for _ in range(200):
            n = rng.randrange(0, 200)
            a, b = sorted([rng.random(), rng.random()])
            train, val, test = train_val_test_split(n, (a, b - a, 1 - b), seed=1)
            self.assertEqual(len(train) + len(val) + len(test), n)

    def test_matches_the_specified_recipe(self):
        order = list(range(100))
        random.Random(42).shuffle(order)
        self.assertEqual(train_val_test_split(100, (0.7, 0.2, 0.1), 42), (order[:70], order[70:90], order[90:]))

    def test_seeded_and_shuffled(self):
        a = train_val_test_split(100, (0.8, 0.1, 0.1), seed=3)
        self.assertEqual(a, train_val_test_split(100, (0.8, 0.1, 0.1), seed=3))
        self.assertNotEqual(a, train_val_test_split(100, (0.8, 0.1, 0.1), seed=4))
        self.assertNotEqual(a[0], list(range(80)))

    def test_empty(self):
        self.assertEqual(train_val_test_split(0, (0.6, 0.2, 0.2), seed=0), ([], [], []))

    def test_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            train_val_test_split(5, (0.5, 0.5, 0.5), 0)
        with self.assertRaises(ValueError):
            train_val_test_split(5, (1.2, -0.1, -0.1), 0)
        with self.assertRaises(ValueError):
            train_val_test_split(5, (0.5, 0.5), 0)
        with self.assertRaises(ValueError):
            train_val_test_split(-1, (0.6, 0.2, 0.2), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
