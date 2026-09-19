import random
import unittest

from solution import sample_configs

SPACE = {"lr": ("log", 1e-5, 1e-1), "dropout": ("uniform", 0.0, 0.5), "opt": ("choice", ["sgd", "adam"])}


class TestLogUniformSearch(unittest.TestCase):
    def test_returns_n_configs_with_all_keys(self):
        out = sample_configs(SPACE, 5, random.Random(0))
        self.assertEqual(len(out), 5)
        for cfg in out:
            self.assertEqual(set(cfg), set(SPACE))

    def test_values_stay_in_range(self):
        for cfg in sample_configs(SPACE, 500, random.Random(1)):
            self.assertTrue(1e-5 <= cfg["lr"] <= 1e-1)
            self.assertTrue(0.0 <= cfg["dropout"] <= 0.5)
            self.assertIn(cfg["opt"], ["sgd", "adam"])

    def test_log_range_spreads_evenly_over_decades(self):
        lrs = [c["lr"] for c in sample_configs({"lr": ("log", 1e-5, 1e-1)}, 2000, random.Random(2))]
        for lo in (1e-5, 1e-4, 1e-3, 1e-2):
            frac = sum(lo <= v < lo * 10 for v in lrs) / len(lrs)
            self.assertTrue(0.20 <= frac <= 0.30, msg=f"decade starting {lo}: {frac:.3f}")

    def test_uniform_range_is_not_log_scaled(self):
        vals = [c["x"] for c in sample_configs({"x": ("uniform", 0.0, 1.0)}, 2000, random.Random(3))]
        self.assertAlmostEqual(sum(v < 0.5 for v in vals) / len(vals), 0.5, delta=0.05)
        self.assertLess(sum(v < 0.1 for v in vals) / len(vals), 0.15)

    def test_choices_are_all_used(self):
        opts = {c["opt"] for c in sample_configs({"opt": ("choice", ["a", "b", "c"])}, 200, random.Random(4))}
        self.assertEqual(opts, {"a", "b", "c"})

    def test_same_seed_same_configs(self):
        self.assertEqual(sample_configs(SPACE, 10, random.Random(9)), sample_configs(SPACE, 10, random.Random(9)))
        self.assertNotEqual(sample_configs(SPACE, 10, random.Random(9)), sample_configs(SPACE, 10, random.Random(10)))

    def test_zero_configs(self):
        self.assertEqual(sample_configs(SPACE, 0, random.Random(0)), [])

    def test_rejects_bad_specs(self):
        bad = [
            {"lr": ("log", 0.0, 1.0)},
            {"lr": ("log", 1e-1, 1e-5)},
            {"x": ("uniform", 1.0, 1.0)},
            {"o": ("choice", [])},
            {"z": ("normal", 0.0, 1.0)},
        ]
        for space in bad:
            with self.assertRaises(ValueError, msg=str(space)):
                sample_configs(space, 0, random.Random(0))
        with self.assertRaises(ValueError):
            sample_configs(SPACE, -1, random.Random(0))


if __name__ == "__main__":
    unittest.main(verbosity=2)
