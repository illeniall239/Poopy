import math
import unittest

from solution import simulate_depth_std


class TestSimulateDepthStd(unittest.TestCase):
    def test_returns_one_float_per_layer(self):
        stds = simulate_depth_std(7, 32, 0.2, "tanh", 0)
        self.assertEqual(len(stds), 7)
        self.assertTrue(all(type(s) is float for s in stds))

    def test_linear_with_one_over_sqrt_width_is_stable(self):
        stds = simulate_depth_std(20, 100, 0.1, "linear", 0)
        self.assertTrue(all(0.7 < s < 1.4 for s in stds), msg=str(stds))

    def test_linear_with_unit_std_explodes(self):
        stds = simulate_depth_std(10, 100, 1.0, "linear", 0)
        for prev, cur in zip(stds, stds[1:]):
            self.assertTrue(8.0 < cur / prev < 12.5, msg=f"{prev} -> {cur}")
        self.assertGreater(stds[-1], 1e9)

    def test_small_tanh_init_collapses(self):
        stds = simulate_depth_std(20, 100, 0.01, "tanh", 0)
        self.assertTrue(all(a > b for a, b in zip(stds, stds[1:])))
        self.assertLess(stds[-1], 1e-15)

    def test_large_tanh_init_saturates(self):
        stds = simulate_depth_std(20, 100, 1.0, "tanh", 0)
        self.assertTrue(all(0.85 < s <= 1.0 for s in stds[1:]), msg=str(stds))

    def test_records_std_after_the_activation(self):
        (s,) = simulate_depth_std(1, 256, 1 / 16, "relu", 0)
        self.assertAlmostEqual(s, math.sqrt(0.5 - 1 / (2 * math.pi)), delta=0.03)

    def test_kaiming_keeps_relu_alive_but_small_init_does_not(self):
        kaiming = simulate_depth_std(20, 128, math.sqrt(2 / 128), "relu", 1)
        naive = simulate_depth_std(20, 128, 0.01, "relu", 1)
        self.assertTrue(0.3 < kaiming[-1] / kaiming[0] < 3.0, msg=str(kaiming))
        self.assertLess(naive[-1], 1e-10)

    def test_seeded(self):
        a = simulate_depth_std(5, 16, 0.3, "tanh", 42)
        self.assertEqual(a, simulate_depth_std(5, 16, 0.3, "tanh", 42))
        self.assertNotEqual(a, simulate_depth_std(5, 16, 0.3, "tanh", 43))

    def test_rejects_bad_arguments(self):
        for args in [(3, 10, 0.1, "sigmoid", 0), (0, 10, 0.1, "relu", 0), (3, 0, 0.1, "relu", 0), (3, 10, 0.0, "relu", 0)]:
            with self.assertRaises(ValueError, msg=str(args)):
                simulate_depth_std(*args)


if __name__ == "__main__":
    unittest.main(verbosity=2)
