import random
import unittest

from solution import best_split


class TestBestSplit(unittest.TestCase):
    def assertSplit(self, got, feature, threshold, gain):
        self.assertIsNotNone(got)
        self.assertEqual(got[0], feature)
        self.assertAlmostEqual(got[1], threshold, places=12)
        self.assertAlmostEqual(got[2], gain, places=9)

    def test_simple_separable(self):
        self.assertSplit(best_split([[1.0], [2.0], [3.0], [4.0]], [0, 0, 1, 1]), 0, 2.5, 0.5)

    def test_threshold_is_a_midpoint(self):
        self.assertSplit(best_split([[1.0], [3.0]], ["a", "b"]), 0, 2.0, 0.5)
        # duplicates collapse: candidates for [3, 1, 3, 5] are 2.0 and 4.0
        self.assertSplit(best_split([[3.0], [1.0], [3.0], [5.0]], [1, 0, 1, 1]), 0, 2.0, 0.375)

    def test_children_are_weighted_by_size(self):
        # Unweighted averaging would isolate the first row at 1.5 instead.
        X = [[float(x)] for x in range(1, 9)]
        self.assertSplit(best_split(X, [0, 0, 0, 0, 1, 1, 0, 0]), 0, 4.5, 0.125)

    def test_picks_the_informative_feature(self):
        X = [[5.0, 1.0], [1.0, 2.0], [4.0, 3.0], [2.0, 4.0], [3.0, 10.0]]
        y = ["n", "n", "y", "y", "y"]
        self.assertSplit(best_split(X, y), 1, 2.5, 0.48)

    def test_ties_go_to_smaller_feature_then_threshold(self):
        X = [[1.0, 1.0], [2.0, 2.0], [3.0, 3.0], [4.0, 4.0]]
        self.assertSplit(best_split(X, [0, 0, 1, 1]), 0, 2.5, 0.5)
        # Two thresholds with equal gain on one feature: 1.5 and 2.5 both give gain 1/9.
        self.assertSplit(best_split([[1.0], [2.0], [3.0]], [0, 1, 0]), 0, 1.5, 1 / 9)

    def test_none_when_no_useful_split(self):
        self.assertIsNone(best_split([[1.0, 5.0], [2.0, 5.0]], [0, 0]))
        self.assertIsNone(best_split([[1.0, 5.0], [1.0, 5.0]], [0, 1]))
        self.assertIsNone(best_split([[7.0]], [1]))

    def test_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            best_split([], [])
        with self.assertRaises(ValueError):
            best_split([[1.0], [2.0]], [0])

    def test_matches_a_sklearn_stump(self):
        from sklearn.tree import DecisionTreeClassifier

        rng = random.Random(11)
        for _ in range(5):
            X = [[rng.uniform(-3, 3) for _ in range(3)] for _ in range(60)]
            y = [int(r[1] + 0.5 * rng.gauss(0, 1) > 0) + int(r[2] > 1.5) for r in X]
            stump = DecisionTreeClassifier(max_depth=1, criterion="gini").fit(X, y)
            feature, threshold, gain = best_split(X, y)
            self.assertEqual(feature, stump.tree_.feature[0])
            self.assertAlmostEqual(threshold, stump.tree_.threshold[0], places=5)  # sklearn stores float32
            t = stump.tree_
            expected = t.impurity[0] - sum(
                t.n_node_samples[c] / t.n_node_samples[0] * t.impurity[c] for c in (t.children_left[0], t.children_right[0])
            )
            self.assertAlmostEqual(gain, expected, places=9)


if __name__ == "__main__":
    unittest.main(verbosity=2)
