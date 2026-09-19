import math
import random
import unittest

from solution import random_search

SPACE = {"lr": ("loguniform", 1e-5, 1e-1), "depth": [2, 4, 8], "dropout": ("uniform", 0.0, 0.5)}


class TestRandomSearch(unittest.TestCase):
    def test_same_seed_same_configurations(self):
        a = random_search(SPACE, 20, random.Random(0))
        b = random_search(SPACE, 20, random.Random(0))
        self.assertEqual(a, b)
        self.assertNotEqual(a, random_search(SPACE, 20, random.Random(1)))

    def test_exact_rng_call_order(self):
        rng = random.Random(42)
        expected = []
        for _ in range(5):
            expected.append({
                "depth": rng.choice([2, 4, 8]),
                "dropout": rng.uniform(0.0, 0.5),
                "lr": math.exp(rng.uniform(math.log(1e-5), math.log(1e-1))),
            })
        got = random_search(SPACE, 5, random.Random(42))
        self.assertEqual(len(got), 5)
        for g, e in zip(got, expected):
            self.assertEqual(g["depth"], e["depth"])
            self.assertAlmostEqual(g["dropout"], e["dropout"], places=12)
            self.assertAlmostEqual(math.log(g["lr"]), math.log(e["lr"]), places=9)

    def test_order_ignores_dict_insertion_order(self):
        reordered = {"dropout": SPACE["dropout"], "lr": SPACE["lr"], "depth": SPACE["depth"]}
        self.assertEqual(random_search(SPACE, 10, random.Random(3)), random_search(reordered, 10, random.Random(3)))

    def test_values_stay_in_range_and_choices_are_covered(self):
        configs = random_search(SPACE, 500, random.Random(7))
        self.assertTrue(all(c["depth"] in (2, 4, 8) for c in configs))
        self.assertEqual({c["depth"] for c in configs}, {2, 4, 8})
        self.assertTrue(all(0.0 <= c["dropout"] <= 0.5 for c in configs))
        self.assertTrue(all(1e-5 <= c["lr"] <= 1e-1 for c in configs))
        self.assertEqual(set(configs[0]), {"depth", "dropout", "lr"})

    def test_loguniform_spreads_over_orders_of_magnitude(self):
        lrs = [c["lr"] for c in random_search({"lr": ("loguniform", 1e-5, 1e-1)}, 4000, random.Random(11))]
        below = sum(lr < 1e-3 for lr in lrs) / len(lrs)
        self.assertGreater(below, 0.45)  # plain uniform would put about 1% here
        self.assertLess(below, 0.55)
        per_decade = [sum(10.0 ** -(k + 1) <= lr < 10.0 ** -k for lr in lrs) for k in range(1, 5)]
        self.assertTrue(all(800 < c < 1200 for c in per_decade), per_decade)

    def test_zero_configurations(self):
        self.assertEqual(random_search(SPACE, 0, random.Random(0)), [])

    def test_rejects_bad_space_before_drawing(self):
        bad_spaces = [
            {"lr": ("loguniform", 0.0, 1.0)},
            {"lr": ("loguniform", -1.0, 1.0)},
            {"lr": ("normal", 0.0, 1.0)},
            {"lr": ("uniform", 1.0, 0.5)},
            {"lr": ("uniform", 0.0)},
            {"depth": []},
            {"depth": 4},
        ]
        for space in bad_spaces:
            rng = random.Random(0)
            state = rng.getstate()
            with self.assertRaises(ValueError, msg=str(space)):
                random_search({"a": [1, 2], **space}, 3, rng)
            self.assertEqual(rng.getstate(), state, msg=str(space))
        with self.assertRaises(ValueError):
            random_search(SPACE, -1, random.Random(0))


if __name__ == "__main__":
    unittest.main(verbosity=2)
