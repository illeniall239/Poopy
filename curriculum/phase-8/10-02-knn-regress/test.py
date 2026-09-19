import unittest

import numpy as np
from sklearn.neighbors import KNeighborsRegressor

from solution import knn_regress

STRICT = dict(over="raise", divide="raise", invalid="raise")
TX = np.array([[0.0], [1.0], [3.0], [10.0]])
TY = np.array([0.0, 10.0, 30.0, 100.0])


class TestKnnRegress(unittest.TestCase):
    def test_unweighted_mean(self):
        self.assertAlmostEqual(knn_regress(TX, TY, np.array([0.5]), 2), 5.0, places=9)
        self.assertAlmostEqual(knn_regress(TX, TY, np.array([1.0]), 3), 40.0 / 3, places=9)
        self.assertAlmostEqual(knn_regress(TX, TY, np.array([-50.0]), 4), 35.0, places=9)
        self.assertIsInstance(knn_regress(TX, TY, np.array([0.5]), 2), float)

    def test_inverse_distance_weights(self):
        self.assertAlmostEqual(knn_regress(TX, TY, np.array([0.25]), 2, weighted=True), 2.5, places=9)
        # distances 2, 1, 1 -> weights 1/2, 1, 1 for targets 0, 10, 30 -> 40 / 2.5
        self.assertAlmostEqual(knn_regress(TX, TY, np.array([2.0]), 3, weighted=True), 16.0, places=9)

    def test_zero_distance_guard(self):
        with np.errstate(**STRICT):
            self.assertAlmostEqual(knn_regress(TX, TY, np.array([1.0]), 3, weighted=True), 10.0, places=9)
            out = knn_regress(np.array([[2.0], [2.0], [5.0]]), np.array([1.0, 3.0, 9.0]), np.array([2.0]), 3, weighted=True)
        self.assertAlmostEqual(out, 2.0, places=9)

    def test_neighbor_choice_uses_index_on_equal_distance(self):
        X = np.array([[0.0], [2.0], [-2.0]])
        y = np.array([0.0, 5.0, 100.0])
        self.assertAlmostEqual(knn_regress(X, y, np.array([0.0]), 2), 2.5, places=9)
        self.assertAlmostEqual(knn_regress(X, y, np.array([0.0]), 3), 35.0, places=9)

    def test_matches_sklearn(self):
        rng = np.random.default_rng(0)
        X = rng.normal(size=(400, 3))
        y = np.sin(X[:, 0]) + X[:, 1] ** 2 + 0.1 * rng.normal(size=400)
        queries = np.vstack([rng.normal(size=(40, 3)), X[:5]])  # the last 5 sit exactly on training points
        for weights in ["uniform", "distance"]:
            for k in [1, 5, 20]:
                model = KNeighborsRegressor(n_neighbors=k, weights=weights).fit(X, y)
                expected = model.predict(queries)
                got = np.array([knn_regress(X, y, q, k, weighted=(weights == "distance")) for q in queries])
                np.testing.assert_allclose(got, expected, atol=1e-9)

    def test_k_equals_n_predicts_the_global_mean(self):
        rng = np.random.default_rng(1)
        X = rng.normal(size=(50, 2))
        y = rng.normal(size=50)
        for q in rng.normal(size=(5, 2)):
            self.assertAlmostEqual(knn_regress(X, y, q, 50), float(y.mean()), places=9)

    def test_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            knn_regress(TX, TY, np.array([0.5]), 0)
        with self.assertRaises(ValueError):
            knn_regress(TX, TY, np.array([0.5]), 5)
        with self.assertRaises(ValueError):
            knn_regress(TX, TY[:-1], np.array([0.5]), 1)
        with self.assertRaises(ValueError):
            knn_regress(TX, TY, np.array([0.5, 1.0]), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
