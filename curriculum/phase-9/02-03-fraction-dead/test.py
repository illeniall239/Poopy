import unittest

import numpy as np

from solution import fraction_dead


class TestFractionDead(unittest.TestCase):
    def test_example(self):
        self.assertAlmostEqual(fraction_dead([[1.0, -2.0, 0.0], [-1.0, -0.5, 0.0]]), 2 / 3)

    def test_returns_float(self):
        self.assertIsInstance(fraction_dead([[-1.0, 3.0]]), float)
        self.assertEqual(fraction_dead([[-1.0, 3.0]]), 0.5)

    def test_one_firing_example_keeps_a_unit_alive(self):
        self.assertEqual(fraction_dead([[0.1, -1.0], [-5.0, 2.0]]), 0.0)
        # mostly negative, one tiny positive: alive
        self.assertEqual(fraction_dead([[-3.0], [-2.0], [-9.0], [1e-9]]), 0.0)

    def test_zero_counts_as_not_firing(self):
        self.assertEqual(fraction_dead([[0.0, 0.0], [0.0, 1.0]]), 0.5)

    def test_counts_columns_not_rows_or_entries(self):
        # 3 examples x 4 units: rows 0 and 2 are all <= 0, but only unit 3 is dead.
        m = [[-1.0, -1.0, -1.0, -1.0],
             [2.0, 3.0, 4.0, -1.0],
             [-1.0, -1.0, 0.0, 0.0]]
        self.assertEqual(fraction_dead(m), 0.25)

    def test_accepts_numpy_array(self):
        rng = np.random.default_rng(0)
        z = rng.normal(size=(50, 8))
        z[:, [1, 4, 5]] = -np.abs(z[:, [1, 4, 5]])
        z[0, :] = np.abs(z[0, :])
        z[0, [1, 4, 5]] *= -1
        self.assertAlmostEqual(fraction_dead(z), 3 / 8)

    def test_bad_input(self):
        for bad in ([], [[]], [[1.0, 2.0], [3.0]]):
            with self.assertRaises(ValueError, msg=repr(bad)):
                fraction_dead(bad)


if __name__ == "__main__":
    unittest.main(verbosity=2)
