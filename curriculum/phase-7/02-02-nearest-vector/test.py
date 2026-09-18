import unittest

import numpy as np

from solution import nearest_by_cosine, nearest_by_euclidean


class TestNearestVector(unittest.TestCase):
    def test_measures_disagree(self):
        vectors = [[10.0, 10.0], [1.2, 0.8], [-1.0, -1.0]]
        self.assertEqual(nearest_by_euclidean([1.0, 1.0], vectors), 1)
        self.assertEqual(nearest_by_cosine([1.0, 1.0], vectors), 0)

    def test_measures_agree_on_unit_vectors(self):
        vectors = [[1.0, 0.0], [0.0, 1.0], [-1.0, 0.0]]
        self.assertEqual(nearest_by_euclidean([0.9, 0.1], vectors), 0)
        self.assertEqual(nearest_by_cosine([0.9, 0.1], vectors), 0)
        self.assertEqual(nearest_by_euclidean([0.1, 0.9], vectors), 1)
        self.assertEqual(nearest_by_cosine([0.1, 0.9], vectors), 1)

    def test_ties_return_smallest_index(self):
        self.assertEqual(nearest_by_euclidean([0.0, 0.0], [[1.0, 0.0], [0.0, 1.0]]), 0)
        self.assertEqual(nearest_by_cosine([1.0, 1.0], [[2.0, 2.0], [2.0, 2.0]]), 0)

    def test_exact_match_wins(self):
        vectors = [[3.0, 4.0], [1.0, 2.0], [5.0, 5.0]]
        self.assertEqual(nearest_by_euclidean([1.0, 2.0], vectors), 1)
        self.assertEqual(nearest_by_cosine([1.0, 2.0], vectors), 1)

    def test_opposite_direction_is_worst_for_cosine(self):
        vectors = [[-1.0, -1.0], [0.0, 1.0]]
        self.assertEqual(nearest_by_cosine([1.0, 1.0], vectors), 1)

    def test_empty_and_mismatch_raise(self):
        with self.assertRaises(ValueError):
            nearest_by_euclidean([1.0], [])
        with self.assertRaises(ValueError):
            nearest_by_cosine([1.0], [])
        with self.assertRaises(ValueError):
            nearest_by_euclidean([1.0, 2.0], [[1.0]])
        with self.assertRaises(ValueError):
            nearest_by_cosine([1.0, 2.0], [[1.0]])

    def test_zero_vector_rejected_for_cosine_only(self):
        with self.assertRaises(ValueError):
            nearest_by_cosine([1.0, 0.0], [[0.0, 0.0]])
        with self.assertRaises(ValueError):
            nearest_by_cosine([0.0, 0.0], [[1.0, 0.0]])
        self.assertEqual(nearest_by_euclidean([0.0, 0.0], [[0.0, 0.0]]), 0)

    def test_matches_numpy_on_random_data(self):
        rng = np.random.default_rng(0)
        for _ in range(5):
            q = rng.normal(size=6)
            vs = rng.normal(size=(200, 6))
            d = np.linalg.norm(vs - q, axis=1)
            c = vs @ q / (np.linalg.norm(vs, axis=1) * np.linalg.norm(q))
            self.assertEqual(nearest_by_euclidean(list(q), vs.tolist()), int(d.argmin()))
            self.assertEqual(nearest_by_cosine(list(q), vs.tolist()), int(c.argmax()))


if __name__ == "__main__":
    unittest.main(verbosity=2)
