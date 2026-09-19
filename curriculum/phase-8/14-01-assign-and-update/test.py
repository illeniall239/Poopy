import unittest

import numpy as np

from solution import assign, update

POINTS = np.array([[0.0, 0.0], [1.0, 0.0], [9.0, 9.0], [10.0, 9.0]])
CENTROIDS = np.array([[0.0, 1.0], [9.0, 8.0]])


def inertia(points, labels, centroids):
    return float(((points - centroids[labels]) ** 2).sum())


class TestAssignAndUpdate(unittest.TestCase):
    def test_assign_small(self):
        got = assign(POINTS, CENTROIDS)
        self.assertEqual(got.shape, (4,))
        self.assertTrue(np.issubdtype(got.dtype, np.integer))
        self.assertEqual(got.tolist(), [0, 0, 1, 1])

    def test_assign_tie_goes_to_smaller_index(self):
        self.assertEqual(assign(np.array([[1.0]]), np.array([[0.0], [2.0]])).tolist(), [0])
        self.assertEqual(assign(np.array([[1.0, 1.0]]), np.array([[5.0, 5.0], [2.0, 0.0], [0.0, 2.0]])).tolist(), [1])

    def test_assign_matches_brute_force(self):
        rng = np.random.default_rng(0)
        points, centroids = rng.normal(size=(500, 3)), rng.normal(size=(6, 3))
        expected = [int(np.argmin([np.linalg.norm(p - c) for c in centroids])) for p in points]
        self.assertEqual(assign(points, centroids).tolist(), expected)

    def test_update_means(self):
        got = update(POINTS, np.array([0, 0, 1, 1]), 2, CENTROIDS)
        np.testing.assert_allclose(got, [[0.5, 0.0], [9.5, 9.0]], atol=1e-12)
        rng = np.random.default_rng(1)
        pts = rng.normal(size=(200, 2))
        labels = rng.integers(0, 4, size=200)
        got = update(pts, labels, 4, np.zeros((4, 2)))
        for c in range(4):
            np.testing.assert_allclose(got[c], pts[labels == c].mean(axis=0), atol=1e-12)

    def test_empty_cluster_keeps_its_old_centroid(self):
        old = CENTROIDS.copy()
        got = update(POINTS, np.array([0, 0, 0, 0]), 2, old)
        np.testing.assert_allclose(got, [[5.0, 4.5], [9.0, 8.0]], atol=1e-12)
        self.assertFalse(np.isnan(got).any())
        np.testing.assert_array_equal(old, CENTROIDS)
        self.assertIsNot(got, old)

    def test_one_round_never_increases_inertia(self):
        rng = np.random.default_rng(2)
        points = rng.normal(size=(300, 2))
        centroids = rng.normal(size=(5, 2)) * 3
        labels = assign(points, centroids)
        before = inertia(points, labels, centroids)
        new = update(points, labels, 5, centroids)
        mid = inertia(points, labels, new)
        after = inertia(points, assign(points, new), new)
        self.assertLessEqual(mid, before + 1e-9)
        self.assertLessEqual(after, mid + 1e-9)

    def test_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            assign(POINTS, np.zeros((2, 3)))
        with self.assertRaises(ValueError):
            assign(POINTS[:, 0], CENTROIDS)
        with self.assertRaises(ValueError):
            assign(POINTS, np.zeros((0, 2)))
        with self.assertRaises(ValueError):
            update(POINTS, np.array([0, 1, 0]), 2, CENTROIDS)
        with self.assertRaises(ValueError):
            update(POINTS, np.array([0, 1, 2, 0]), 2, CENTROIDS)
        with self.assertRaises(ValueError):
            update(POINTS, np.array([0, 1, 1, 0]), 3, CENTROIDS)


if __name__ == "__main__":
    unittest.main(verbosity=2)
