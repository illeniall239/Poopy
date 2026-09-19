import unittest

from sklearn.model_selection import KFold

from solution import kfold_indices


class TestKfoldIndices(unittest.TestCase):
    def test_ten_by_three(self):
        self.assertEqual(
            kfold_indices(10, 3),
            [
                ([4, 5, 6, 7, 8, 9], [0, 1, 2, 3]),
                ([0, 1, 2, 3, 7, 8, 9], [4, 5, 6]),
                ([0, 1, 2, 3, 4, 5, 6], [7, 8, 9]),
            ],
        )

    def test_leave_one_out(self):
        folds = kfold_indices(5, 5)
        self.assertEqual(len(folds), 5)
        for i, (train, val) in enumerate(folds):
            self.assertEqual(val, [i])
            self.assertEqual(train, [j for j in range(5) if j != i])

    def test_every_index_in_exactly_one_validation_fold(self):
        for n, k in [(10, 3), (11, 4), (100, 7), (7, 2), (13, 13)]:
            folds = kfold_indices(n, k)
            self.assertEqual(len(folds), k)
            all_val = [i for _, val in folds for i in val]
            self.assertEqual(sorted(all_val), list(range(n)), (n, k))

    def test_train_is_the_complement(self):
        for n, k in [(10, 3), (23, 5)]:
            for train, val in kfold_indices(n, k):
                self.assertFalse(set(train) & set(val))
                self.assertEqual(sorted(train + val), list(range(n)))
                self.assertEqual(train, sorted(train))

    def test_sizes_differ_by_at_most_one_larger_first(self):
        for n, k in [(10, 3), (11, 4), (100, 7), (99, 10)]:
            sizes = [len(val) for _, val in kfold_indices(n, k)]
            self.assertLessEqual(max(sizes) - min(sizes), 1)
            self.assertEqual(sizes, sorted(sizes, reverse=True))

    def test_matches_sklearn(self):
        for n, k in [(10, 3), (37, 5), (50, 10), (8, 8)]:
            expected = [(tr.tolist(), va.tolist()) for tr, va in KFold(n_splits=k).split(list(range(n)))]
            self.assertEqual(kfold_indices(n, k), expected, (n, k))

    def test_large_is_fast_enough(self):
        folds = kfold_indices(20000, 10)
        self.assertEqual(sum(len(val) for _, val in folds), 20000)
        self.assertEqual(len(folds[0][0]), 18000)

    def test_rejects_bad_k(self):
        with self.assertRaises(ValueError):
            kfold_indices(4, 1)
        with self.assertRaises(ValueError):
            kfold_indices(3, 4)
        with self.assertRaises(ValueError):
            kfold_indices(0, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
