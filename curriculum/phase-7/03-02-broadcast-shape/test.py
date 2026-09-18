import unittest

import numpy as np

from solution import broadcast_shape


class TestBroadcastShape(unittest.TestCase):
    def test_row_vector_against_matrix(self):
        self.assertEqual(broadcast_shape((3, 4), (4,)), (3, 4))
        self.assertEqual(broadcast_shape((4,), (3, 4)), (3, 4))

    def test_both_sides_stretch(self):
        self.assertEqual(broadcast_shape((3, 1), (1, 4)), (3, 4))

    def test_silent_outer_product_shape(self):
        self.assertEqual(broadcast_shape((3,), (3, 1)), (3, 3))

    def test_leading_dimension_padding(self):
        self.assertEqual(broadcast_shape((2, 1, 5), (7, 1)), (2, 7, 5))
        self.assertEqual(broadcast_shape((5,), (2, 3, 5)), (2, 3, 5))

    def test_scalar_shape(self):
        self.assertEqual(broadcast_shape((), (6, 2)), (6, 2))
        self.assertEqual(broadcast_shape((6, 2), ()), (6, 2))
        self.assertEqual(broadcast_shape((), ()), ())

    def test_returns_tuple(self):
        self.assertIsInstance(broadcast_shape((2, 3), (3,)), tuple)

    def test_incompatible_raises(self):
        for a, b in [((3,), (4,)), ((2, 3), (3, 2)), ((2, 3, 4), (3, 3))]:
            with self.assertRaises(ValueError):
                broadcast_shape(a, b)

    def test_matches_numpy_on_random_shapes(self):
        rng = np.random.default_rng(0)
        for _ in range(200):
            a = tuple(int(x) for x in rng.choice([1, 2, 3, 5], size=rng.integers(0, 5)))
            b = tuple(int(x) for x in rng.choice([1, 2, 3, 5], size=rng.integers(0, 5)))
            try:
                expected = np.broadcast_shapes(a, b)
            except ValueError:
                with self.assertRaises(ValueError):
                    broadcast_shape(a, b)
            else:
                self.assertEqual(broadcast_shape(a, b), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
