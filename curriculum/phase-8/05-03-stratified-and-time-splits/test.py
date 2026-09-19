import random
import unittest
from collections import Counter

from sklearn.model_selection import TimeSeriesSplit

from solution import stratified_split, time_series_splits


def rare_labels(n, positives, seed):
    labels = [1] * positives + [0] * (n - positives)
    random.Random(seed).shuffle(labels)
    return labels


class TestStratifiedSplit(unittest.TestCase):
    def test_example(self):
        labels = [0] * 90 + [1] * 10
        train, val = stratified_split(labels, 0.2, seed=0)
        self.assertEqual(len(val), 20)
        self.assertEqual(sum(labels[i] for i in val), 2)
        self.assertEqual(sorted(train + val), list(range(100)))
        self.assertEqual(train, sorted(train))
        self.assertEqual(val, sorted(val))

    def test_rare_class_ratio_holds_for_every_seed(self):
        labels = rare_labels(1000, 20, seed=1)
        for seed in range(30):
            _, val = stratified_split(labels, 0.2, seed)
            self.assertIn(sum(labels[i] for i in val), (3, 4, 5), seed)

    def test_each_class_within_one_row(self):
        rng = random.Random(2)
        labels = [rng.choice(["cat", "dog", "dog", "bird", "fish", "fish", "fish"]) for _ in range(503)]
        counts = Counter(labels)
        for frac in (0.1, 0.25, 0.5, 0.9):
            train, val = stratified_split(labels, frac, seed=3)
            val_counts = Counter(labels[i] for i in val)
            for label, count in counts.items():
                self.assertLessEqual(abs(val_counts[label] - count * frac), 1.0, (label, frac))
            self.assertFalse(set(train) & set(val))
            self.assertEqual(len(train) + len(val), len(labels))

    def test_seeded_and_random(self):
        labels = rare_labels(200, 40, seed=4)
        a = stratified_split(labels, 0.25, seed=5)
        self.assertEqual(a, stratified_split(labels, 0.25, seed=5))
        self.assertNotEqual(a, stratified_split(labels, 0.25, seed=6))
        # Not just the first rows of each class.
        first_positives = [i for i, y in enumerate(labels) if y == 1][:10]
        self.assertNotEqual([i for i in a[1] if labels[i] == 1], first_positives)

    def test_stratified_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            stratified_split([], 0.2, 0)
        for frac in (0.0, 1.0, -0.1, 1.5):
            with self.assertRaises(ValueError):
                stratified_split([0, 1, 0, 1], frac, 0)


class TestTimeSeriesSplits(unittest.TestCase):
    def test_example(self):
        self.assertEqual(
            time_series_splits(10, 3),
            [([0, 1, 2, 3], [4, 5]), ([0, 1, 2, 3, 4, 5], [6, 7]), ([0, 1, 2, 3, 4, 5, 6, 7], [8, 9])],
        )

    def test_validation_always_follows_training(self):
        for n, s in [(10, 3), (100, 5), (7, 6), (50, 1), (101, 4)]:
            splits = time_series_splits(n, s)
            self.assertEqual(len(splits), s)
            for (train, val), (next_train, _) in zip(splits, splits[1:] + [(list(range(n)), None)]):
                self.assertLess(max(train), min(val))
                self.assertEqual(train, list(range(len(train))))  # a prefix of the past, unshuffled
                self.assertEqual(val, list(range(val[0], val[-1] + 1)))
                self.assertGreater(len(next_train), len(train))
            self.assertEqual(splits[-1][1][-1], n - 1)
            vals = [i for _, val in splits for i in val]
            self.assertEqual(len(vals), len(set(vals)))

    def test_matches_sklearn(self):
        for n, s in [(10, 3), (100, 5), (57, 4), (12, 2), (9, 8)]:
            expected = [(tr.tolist(), va.tolist()) for tr, va in TimeSeriesSplit(n_splits=s).split(list(range(n)))]
            self.assertEqual(time_series_splits(n, s), expected, (n, s))

    def test_time_series_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            time_series_splits(3, 3)
        with self.assertRaises(ValueError):
            time_series_splits(10, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
