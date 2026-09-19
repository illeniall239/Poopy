import unittest

import numpy as np
from sklearn.neighbors import KNeighborsClassifier

from solution import knn_predict

TX = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [5.0, 5.0], [6.0, 5.0]])
TY = np.array([0, 0, 0, 1, 1])


class TestKnnClassify(unittest.TestCase):
    def test_simple_majority(self):
        self.assertEqual(knn_predict(TX, TY, np.array([0.2, 0.2]), 3), 0)
        self.assertEqual(knn_predict(TX, TY, np.array([5.5, 5.0]), 1), 1)
        self.assertEqual(knn_predict(TX, TY, np.array([5.5, 5.0]), 2), 1)
        self.assertEqual(knn_predict(TX, TY, np.array([5.5, 5.0]), 5), 0)
        self.assertIsInstance(knn_predict(TX, TY, np.array([0.2, 0.2]), 3), int)

    def test_vote_tie_goes_to_nearest_member(self):
        self.assertEqual(knn_predict(np.array([[0.0], [2.0], [3.0]]), np.array([7, 4, 4]), np.array([1.1]), 2), 4)
        self.assertEqual(knn_predict(np.array([[0.0], [2.0], [3.0]]), np.array([7, 4, 4]), np.array([0.9]), 2), 7)
        # 2-2 tie between labels 5 and 2; label 1 has the single nearest point but is not tied
        X = np.array([[0.0], [1.0], [-1.1], [1.2], [-1.3]])
        y = np.array([1, 5, 2, 2, 5])
        self.assertEqual(knn_predict(X, y, np.array([0.0]), 5), 5)

    def test_vote_tie_at_equal_distance_goes_to_smallest_label(self):
        self.assertEqual(knn_predict(np.array([[-1.0], [1.0]]), np.array([9, 3]), np.array([0.0]), 2), 3)
        self.assertEqual(knn_predict(np.array([[1.0], [-1.0]]), np.array([3, 9]), np.array([0.0]), 2), 3)

    def test_distance_tie_for_kth_neighbor_uses_index(self):
        # points 1 and 2 are both at distance 1; with k = 2 only index 1 is taken
        X = np.array([[0.0], [1.0], [-1.0]])
        self.assertEqual(knn_predict(X, np.array([4, 4, 8]), np.array([0.0]), 2), 4)
        self.assertEqual(knn_predict(X, np.array([4, 8, 4]), np.array([0.0]), 2), 4)
        # here the tie rule decides: labels 4 and 8 have one vote each, 4's member is nearer
        self.assertEqual(knn_predict(X, np.array([4, 8, 8]), np.array([0.0]), 2), 4)
        self.assertEqual(knn_predict(X[1:], np.array([8, 6]), np.array([0.0]), 1), 8)

    def test_matches_sklearn_without_ties(self):
        rng = np.random.default_rng(0)
        X = rng.normal(size=(300, 4))
        y = (X[:, 0] + 0.5 * rng.normal(size=300) > 0).astype(int)
        queries = rng.normal(size=(60, 4))
        for k in [1, 3, 7, 15]:
            model = KNeighborsClassifier(n_neighbors=k).fit(X, y)
            expected = model.predict(queries)
            got = [knn_predict(X, y, q, k) for q in queries]
            self.assertEqual(got, expected.tolist())

    def test_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            knn_predict(TX, TY, np.array([0.0, 0.0]), 0)
        with self.assertRaises(ValueError):
            knn_predict(TX, TY, np.array([0.0, 0.0]), 6)
        with self.assertRaises(ValueError):
            knn_predict(TX, TY[:-1], np.array([0.0, 0.0]), 1)
        with self.assertRaises(ValueError):
            knn_predict(TX, TY, np.array([0.0, 0.0, 0.0]), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
