import unittest

import numpy as np

from solution import kmeans

CENTERS = np.array([[0.0, 0.0], [10.0, 0.0], [0.0, 10.0]])


def blobs(seed=0, spread=0.7, per=30):
    rng = np.random.default_rng(seed)
    return np.vstack([c + rng.normal(scale=spread, size=(per, 2)) for c in CENTERS])


def messy(seed):
    return np.random.default_rng(seed).normal(size=(150, 2)) * np.array([3.0, 1.0])


class TestKMeans(unittest.TestCase):
    def test_recovers_three_blobs(self):
        points = blobs()
        for seed in range(5):
            centroids, labels, history = kmeans(points, 3, seed)
            self.assertEqual(centroids.shape, (3, 2))
            for true_center in CENTERS:
                self.assertLess(np.min(np.linalg.norm(centroids - true_center, axis=1)), 0.5)
            for b in range(3):  # each true blob lands in exactly one cluster
                self.assertEqual(len(set(labels[30 * b : 30 * (b + 1)].tolist())), 1)
            self.assertEqual(len(set(labels.tolist())), 3)

    def test_inertia_never_increases(self):
        for seed in range(6):
            _, _, history = kmeans(messy(seed), 6, seed)
            self.assertGreater(len(history), 1)
            for before, after in zip(history, history[1:]):
                self.assertLessEqual(after, before + 1e-9)

    def test_history_ends_at_the_final_inertia(self):
        points = messy(1)
        centroids, labels, history = kmeans(points, 4, 0)
        final = float(((points - centroids[labels]) ** 2).sum())
        self.assertAlmostEqual(history[-1], final, places=8)
        dist = ((points[:, None, :] - centroids[None]) ** 2).sum(axis=2)
        self.assertEqual(labels.tolist(), dist.argmin(axis=1).tolist())

    def test_stops_early_and_respects_iters(self):
        points = blobs()
        _, _, history = kmeans(points, 3, 0, iters=100)
        self.assertLess(len(history), 10)
        _, _, history = kmeans(messy(2), 8, 0, iters=2)
        self.assertLessEqual(len(history), 2)

    def test_pinned_init_matches_sklearn_lloyd(self):
        from sklearn.cluster import KMeans

        for seed in range(3):
            points = messy(10 + seed)
            init = points[np.random.default_rng(seed).choice(len(points), size=5, replace=False)]
            ref = KMeans(n_clusters=5, init=init, n_init=1, algorithm="lloyd", tol=0.0, max_iter=300).fit(points)
            centroids, labels, history = kmeans(points, 5, seed, iters=300)
            np.testing.assert_allclose(centroids, ref.cluster_centers_, atol=1e-8)
            self.assertAlmostEqual(history[-1], ref.inertia_, places=6)

    def test_same_seed_same_result(self):
        a = kmeans(messy(3), 4, 7)
        b = kmeans(messy(3), 4, 7)
        np.testing.assert_array_equal(a[0], b[0])
        self.assertEqual(a[2], b[2])

    def test_k_one_is_the_mean_and_duplicates_do_not_make_nan(self):
        points = messy(4)
        centroids, labels, history = kmeans(points, 1, 0)
        np.testing.assert_allclose(centroids[0], points.mean(axis=0), atol=1e-12)
        self.assertEqual(set(labels.tolist()), {0})
        dup = np.array([[0.0, 0.0]] * 5 + [[10.0, 10.0]] * 5)
        centroids, labels, history = kmeans(dup, 3, 0)  # two starting centroids coincide: one cluster stays empty
        self.assertFalse(np.isnan(centroids).any())
        self.assertAlmostEqual(history[-1], 0.0, places=12)

    def test_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            kmeans(np.zeros((3, 2)), 4, 0)
        with self.assertRaises(ValueError):
            kmeans(np.zeros((3, 2)), 0, 0)
        with self.assertRaises(ValueError):
            kmeans(np.zeros(3), 1, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
