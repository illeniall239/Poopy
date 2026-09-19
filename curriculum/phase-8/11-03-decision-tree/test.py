import random
import unittest

from solution import build_tree, predict_tree

# A toy set no single split can fit: label 1 in the top-right block, plus a lone 1 at the bottom-left corner.
TOY_X = [[float(a), float(b)] for a in range(6) for b in range(6)]
TOY_Y = [int((a >= 3 and b >= 2) or (a == 0 and b == 0)) for a, b in TOY_X]


def depth(tree):
    if "value" in tree:
        return 0
    return 1 + max(depth(tree["left"]), depth(tree["right"]))


def accuracy(tree, X, y):
    return sum(predict_tree(tree, x) == t for x, t in zip(X, y)) / len(y)


class TestDecisionTree(unittest.TestCase):
    def test_one_split_shape(self):
        tree = build_tree([[1.0], [2.0], [3.0], [4.0]], [0, 0, 1, 1])
        self.assertEqual(tree["feature"], 0)
        self.assertAlmostEqual(tree["threshold"], 2.5)
        self.assertEqual(tree["left"], {"value": 0})
        self.assertEqual(tree["right"], {"value": 1})

    def test_depth_zero_is_a_majority_leaf_with_tie_to_smallest(self):
        self.assertEqual(build_tree([[1.0], [2.0], [3.0], [4.0]], [0, 0, 1, 1], max_depth=0), {"value": 0})
        self.assertEqual(build_tree([[1.0], [2.0], [3.0]], ["b", "a", "b"], max_depth=0), {"value": "b"})
        self.assertEqual(build_tree([[1.0], [2.0]], ["z", "c"], max_depth=0), {"value": "c"})

    def test_full_depth_fits_the_toy_set(self):
        tree = build_tree(TOY_X, TOY_Y)
        self.assertEqual(accuracy(tree, TOY_X, TOY_Y), 1.0)
        self.assertGreaterEqual(depth(tree), 3)

    def test_depth_one_underfits(self):
        tree = build_tree(TOY_X, TOY_Y, max_depth=1)
        self.assertEqual(depth(tree), 1)
        self.assertLess(accuracy(tree, TOY_X, TOY_Y), 0.9)

    def test_max_depth_is_respected(self):
        rng = random.Random(4)
        X = [[rng.random(), rng.random()] for _ in range(80)]
        y = [rng.randrange(3) for _ in X]
        for d in (1, 2, 3, 4):
            self.assertLessEqual(depth(build_tree(X, y, max_depth=d)), d)
        self.assertEqual(accuracy(build_tree(X, y), X, y), 1.0)

    def test_min_samples_stops_small_nodes(self):
        X = [[float(i)] for i in range(6)]
        y = [0, 1, 0, 1, 0, 1]
        self.assertEqual(build_tree(X, y, min_samples=7), {"value": 0})
        self.assertLess(accuracy(build_tree(X, y, min_samples=3), X, y), 1.0)
        self.assertEqual(accuracy(build_tree(X, y), X, y), 1.0)

    def test_unsplittable_rows_become_a_leaf(self):
        self.assertEqual(build_tree([[1.0], [1.0], [1.0]], ["b", "a", "b"]), {"value": "b"})
        self.assertEqual(build_tree([[2.0, 2.0]] * 4, [1, 0, 0, 1]), {"value": 0})

    def test_no_extrapolation(self):
        X = [[float(x)] for x in range(11)]
        y = ["low"] * 4 + ["mid"] * 4 + ["high"] * 3
        tree = build_tree(X, y)
        self.assertEqual(predict_tree(tree, [50.0]), "high")
        self.assertEqual(predict_tree(tree, [-50.0]), "low")
        self.assertEqual(predict_tree(tree, [3.4]), "low")
        self.assertEqual(predict_tree(tree, [3.6]), "mid")

    def test_matches_sklearn_at_depth_two(self):
        from sklearn.tree import DecisionTreeClassifier

        rng = random.Random(8)
        X = [[rng.uniform(0, 1) for _ in range(3)] for _ in range(120)]
        y = [int(r[0] + r[1] ** 2 + 0.2 * rng.gauss(0, 1) > 0.9) for r in X]
        ours = build_tree(X, y, max_depth=2)
        theirs = DecisionTreeClassifier(max_depth=2).fit(X, y)
        probe = [[rng.uniform(0, 1) for _ in range(3)] for _ in range(300)]
        self.assertEqual([predict_tree(ours, p) for p in probe], [int(v) for v in theirs.predict(probe)])

    def test_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            build_tree([], [])
        with self.assertRaises(ValueError):
            build_tree([[1.0]], [0, 1])
        with self.assertRaises(ValueError):
            build_tree([[1.0]], [0], max_depth=-1)
        with self.assertRaises(ValueError):
            build_tree([[1.0]], [0], min_samples=0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
