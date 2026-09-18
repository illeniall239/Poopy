import unittest

import numpy as np
from numpy.testing import assert_allclose

from solution import project


class TestProject(unittest.TestCase):
    def test_onto_an_axis(self):
        parallel, orthogonal = project([3, 4], [1, 0])
        assert_allclose(parallel, [3.0, 0.0])
        assert_allclose(orthogonal, [0.0, 4.0])

    def test_length_of_b_does_not_matter(self):
        p1, _ = project([3, 4], [1, 0])
        p2, _ = project([3, 4], [2, 0])
        p3, _ = project([3, 4], [0.1, 0])
        assert_allclose(p1, p2)
        assert_allclose(p1, p3)

    def test_a_along_b_and_a_orthogonal_to_b(self):
        parallel, orthogonal = project([1, 1], [1, 1])
        assert_allclose(parallel, [1.0, 1.0])
        assert_allclose(orthogonal, [0.0, 0.0], atol=1e-12)
        parallel, orthogonal = project([1, 0], [0, 1])
        assert_allclose(parallel, [0.0, 0.0], atol=1e-12)
        assert_allclose(orthogonal, [1.0, 0.0])

    def test_projection_can_point_against_b(self):
        parallel, orthogonal = project([2, 2], [-1, 0])
        assert_allclose(parallel, [2.0, 0.0], atol=1e-12)
        assert_allclose(orthogonal, [0.0, 2.0], atol=1e-12)

    def test_parts_add_up_and_are_orthogonal(self):
        rng = np.random.default_rng(0)
        for _ in range(10):
            a = rng.normal(size=7)
            b = rng.normal(size=7)
            parallel, orthogonal = project(list(a), list(b))
            assert_allclose(np.array(parallel) + np.array(orthogonal), a, atol=1e-9)
            self.assertAlmostEqual(float(np.array(orthogonal) @ b), 0.0, places=9)
            self.assertAlmostEqual(float(np.array(parallel) @ orthogonal), 0.0, places=9)

    def test_matches_formula(self):
        rng = np.random.default_rng(1)
        a = rng.normal(size=5)
        b = rng.normal(size=5)
        expected = (a @ b) / (b @ b) * b
        parallel, _ = project(list(a), list(b))
        assert_allclose(parallel, expected, atol=1e-9)

    def test_returns_two_lists_of_same_length(self):
        parallel, orthogonal = project([1.0, 2.0, 3.0], [0.0, 1.0, 0.0])
        self.assertEqual(len(parallel), 3)
        self.assertEqual(len(orthogonal), 3)

    def test_zero_b_and_mismatch_raise(self):
        with self.assertRaises(ValueError):
            project([1, 2], [0, 0])
        with self.assertRaises(ValueError):
            project([1, 2, 3], [1, 2])


if __name__ == "__main__":
    unittest.main(verbosity=2)
