import unittest

import numpy as np

from solution import most_similar

VOCAB = ["cat", "dog", "car", "kitten"]
TABLE = np.array([[1.0, 0.1], [0.9, 0.3], [0.0, 1.0], [10.0, 1.2]])


def cos(a, b):
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))


class TestMostSimilar(unittest.TestCase):
    def test_top_two_for_cat(self):
        result = most_similar("cat", TABLE, VOCAB, 2)
        self.assertEqual([w for w, _ in result], ["kitten", "dog"])
        self.assertAlmostEqual(result[0][1], cos(TABLE[0], TABLE[3]), places=9)
        self.assertAlmostEqual(result[1][1], cos(TABLE[0], TABLE[1]), places=9)
        self.assertIsInstance(result[0][1], float)

    def test_uses_cosine_not_dot_product(self):
        # By dot product kitten (a long vector) would win; by cosine dog is closest to car.
        result = most_similar("car", TABLE, VOCAB, 1)
        self.assertEqual(result[0][0], "dog")
        self.assertAlmostEqual(result[0][1], cos(TABLE[2], TABLE[1]), places=9)

    def test_excludes_query_even_with_identical_twin(self):
        vocab = ["a", "b", "c"]
        table = np.array([[1.0, 0.0], [1.0, 0.0], [0.0, 1.0]])
        result = most_similar("b", table, vocab, 3)
        self.assertEqual([w for w, _ in result], ["a", "c"])
        self.assertAlmostEqual(result[0][1], 1.0, places=9)

    def test_ties_keep_vocabulary_order(self):
        vocab = ["q", "x", "y", "z"]
        table = np.array([[1.0, 0.0], [0.0, 1.0], [0.0, 2.0], [3.0, 0.0]])
        self.assertEqual([w for w, _ in most_similar("q", table, vocab, 3)], ["z", "x", "y"])

    def test_k_larger_than_vocab_and_zero(self):
        self.assertEqual(len(most_similar("cat", TABLE, VOCAB, 10)), 3)
        self.assertEqual(most_similar("cat", TABLE, VOCAB, 0), [])

    def test_matches_brute_force_on_random_table(self):
        rng = np.random.default_rng(0)
        table = rng.normal(size=(30, 5)) * rng.uniform(0.1, 10.0, size=(30, 1))
        vocab = [f"w{i}" for i in range(30)]
        got = most_similar("w7", table, vocab, 5)
        brute = sorted(((vocab[i], cos(table[7], table[i])) for i in range(30) if i != 7), key=lambda p: -p[1])[:5]
        self.assertEqual([w for w, _ in got], [w for w, _ in brute])
        for (_, s1), (_, s2) in zip(got, brute):
            self.assertAlmostEqual(s1, s2, places=9)

    def test_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            most_similar("cow", TABLE, VOCAB, 1)
        with self.assertRaises(ValueError):
            most_similar("cat", TABLE, VOCAB, -1)
        with self.assertRaises(ValueError):
            most_similar("cat", TABLE, VOCAB[:3], 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
