import math
import random
import unittest

from solution import entropy, gini


class TestGiniEntropy(unittest.TestCase):
    def test_pure_node_is_zero(self):
        self.assertAlmostEqual(gini([1, 1, 1, 1]), 0.0, places=12)
        self.assertAlmostEqual(entropy([1, 1, 1, 1]), 0.0, places=12)
        self.assertAlmostEqual(gini(["x"]), 0.0, places=12)
        self.assertAlmostEqual(entropy(["x"]), 0.0, places=12)

    def test_two_classes_balanced(self):
        self.assertAlmostEqual(gini([0, 1]), 0.5, places=12)
        self.assertAlmostEqual(entropy([0, 1, 1, 0]), 1.0, places=12)

    def test_uniform_over_m_classes(self):
        for m in (3, 4, 7):
            labels = list(range(m)) * 5
            self.assertAlmostEqual(gini(labels), 1 - 1 / m, places=12)
            self.assertAlmostEqual(entropy(labels), math.log2(m), places=12)

    def test_hand_computed_unbalanced(self):
        labels = ["a", "a", "a", "b"]
        self.assertAlmostEqual(gini(labels), 0.375, places=12)
        self.assertAlmostEqual(entropy(labels), -(0.75 * math.log2(0.75) + 0.25 * math.log2(0.25)), places=12)

    def test_three_classes_unbalanced(self):
        labels = [0] * 5 + [1] * 3 + [2] * 2
        p = [0.5, 0.3, 0.2]
        self.assertAlmostEqual(gini(labels), 1 - sum(q * q for q in p), places=12)
        self.assertAlmostEqual(entropy(labels), -sum(q * math.log2(q) for q in p), places=12)

    def test_order_does_not_matter(self):
        rng = random.Random(3)
        labels = [rng.choice("abcd") for _ in range(200)]
        shuffled = labels[:]
        rng.shuffle(shuffled)
        self.assertAlmostEqual(gini(labels), gini(shuffled), places=12)
        self.assertAlmostEqual(entropy(labels), entropy(shuffled), places=12)

    def test_uniform_is_the_maximum(self):
        for mix in ([0] * 9 + [1], [0] * 6 + [1] * 4, [0] * 3 + [1] * 7):
            self.assertLess(gini(mix), gini([0, 1]))
            self.assertLess(entropy(mix), entropy([0, 1]))

    def test_empty_raises(self):
        with self.assertRaises(ValueError):
            gini([])
        with self.assertRaises(ValueError):
            entropy([])


if __name__ == "__main__":
    unittest.main(verbosity=2)
