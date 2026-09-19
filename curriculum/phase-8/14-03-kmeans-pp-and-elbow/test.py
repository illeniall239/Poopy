import unittest

import numpy as np

from solution import inertia_curve, kmeans_pp_init


def grid_blobs():
    # Nine tight blobs on a 3 x 3 grid: random init often puts two seeds in one blob.
    rng = np.random.default_rng(0)
    centers = np.array([[10.0 * i, 10.0 * j] for i in range(3) for j in range(3)])
    return np.vstack([c + rng.normal(scale=0.5, size=(20, 2)) for c in centers])


def three_blobs():
    rng = np.random.default_rng(1)
    centers = np.array([[0.0, 0.0], [0.0, 10.0], [0.0, 20.0]])
    return np.vstack([c + rng.normal(scale=0.5, size=(30, 2)) for c in centers])


def lloyd_inertia(points, init):
    from sklearn.cluster import KMeans

    return KMeans(n_clusters=len(init), init=init, n_init=1, algorithm="lloyd", tol=0.0).fit(points).inertia_


class TestKMeansPlusPlus(unittest.TestCase):
    def test_replays_the_pinned_draws(self):
        points = three_blobs()
        for seed in range(3):
            rng = np.random.default_rng(seed)
            chosen = [int(rng.integers(len(points)))]
            for _ in range(3):
                d2 = ((points[:, None, :] - points[chosen][None]) ** 2).sum(axis=2).min(axis=1)
                chosen.append(int(rng.choice(len(points), p=d2 / d2.sum())))
            got = kmeans_pp_init(points, 4, np.random.default_rng(seed))
            np.testing.assert_array_equal(got, points[chosen])

    def test_returns_distinct_data_points(self):
        points = grid_blobs()
        got = kmeans_pp_init(points, 9, np.random.default_rng(4))
        self.assertEqual(got.shape, (9, 2))
        for c in got:
            self.assertTrue(np.any(np.all(points == c, axis=1)))
        self.assertEqual(len({tuple(c) for c in got}), 9)

    def test_spreads_seeds_across_far_clusters(self):
        rng = np.random.default_rng(2)
        points = np.vstack([rng.normal(scale=0.1, size=(50, 2)), rng.normal(scale=0.1, size=(50, 2)) + 100.0])
        for seed in range(20):
            got = kmeans_pp_init(points, 2, np.random.default_rng(seed))
            self.assertEqual(sorted(int(c[0] > 50) for c in got), [0, 1])

    def test_beats_random_init_on_a_hard_case(self):
        points = grid_blobs()
        pp, rand = [], []
        for seed in range(15):
            pp.append(lloyd_inertia(points, kmeans_pp_init(points, 9, np.random.default_rng(seed))))
            idx = np.random.default_rng(seed).choice(len(points), size=9, replace=False)
            rand.append(lloyd_inertia(points, points[idx]))
        best = min(pp + rand)
        self.assertLess(np.mean(pp), 0.5 * np.mean(rand))
        self.assertGreaterEqual(sum(v < best * 1.01 for v in pp), 11)

    def test_rejects_bad_k(self):
        points = three_blobs()
        with self.assertRaises(ValueError):
            kmeans_pp_init(points, 0, np.random.default_rng(0))
        with self.assertRaises(ValueError):
            kmeans_pp_init(points, len(points) + 1, np.random.default_rng(0))
        with self.assertRaises(ValueError):
            kmeans_pp_init(np.array([[1.0, 1.0]] * 5), 2, np.random.default_rng(0))

    def test_inertia_curve_uses_a_fresh_generator_per_k(self):
        points = three_blobs()
        curve = inertia_curve(points, [1, 2, 3, 4, 5], seed=3)
        self.assertEqual(len(curve), 5)
        for k, value in zip([1, 2, 3, 4, 5], curve):
            init = kmeans_pp_init(points, k, np.random.default_rng(3))
            self.assertAlmostEqual(value, lloyd_inertia(points, init), places=6)
        self.assertEqual(curve, inertia_curve(points, [1, 2, 3, 4, 5], seed=3))

    def test_elbow_at_the_true_k(self):
        points = three_blobs()
        c1, c2, c3, c4 = inertia_curve(points, [1, 2, 3, 4], seed=0)
        self.assertAlmostEqual(c1, float(((points - points.mean(axis=0)) ** 2).sum()), places=6)
        self.assertGreater(c1 - c2, 10 * (c3 - c4))
        self.assertGreater(c2 - c3, 10 * (c3 - c4))
        self.assertLess(c3, 0.02 * c1)

    def test_k_equal_to_n_has_zero_inertia(self):
        points = np.array([[0.0, 0.0], [1.0, 0.0], [5.0, 5.0], [9.0, 1.0]])
        self.assertAlmostEqual(inertia_curve(points, [4], seed=0)[0], 0.0, places=12)


if __name__ == "__main__":
    unittest.main(verbosity=2)
