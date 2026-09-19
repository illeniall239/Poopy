import math
import random
import unittest

from solution import bagged_predict, bootstrap_sample


class TestBootstrapAndBagging(unittest.TestCase):
    def test_replays_the_pinned_draws(self):
        in_bag, oob = bootstrap_sample(5, random.Random(0))
        replay = random.Random(0)
        expected = [replay.randrange(5) for _ in range(5)]
        self.assertEqual(in_bag, expected)
        self.assertEqual(oob, sorted(set(range(5)) - set(expected)))

    def test_same_seed_same_sample(self):
        self.assertEqual(bootstrap_sample(50, random.Random(7)), bootstrap_sample(50, random.Random(7)))
        self.assertNotEqual(bootstrap_sample(50, random.Random(7))[0], bootstrap_sample(50, random.Random(8))[0])

    def test_in_bag_and_out_of_bag_partition_the_rows(self):
        rng = random.Random(1)
        for n in (1, 2, 10, 300):
            in_bag, oob = bootstrap_sample(n, rng)
            self.assertEqual(len(in_bag), n)
            self.assertTrue(all(0 <= i < n for i in in_bag))
            self.assertEqual(oob, sorted(oob))
            self.assertEqual(set(in_bag) | set(oob), set(range(n)))
            self.assertFalse(set(in_bag) & set(oob))

    def test_drawn_with_replacement(self):
        rng = random.Random(2)
        fractions = []
        for _ in range(20):
            in_bag, oob = bootstrap_sample(2000, rng)
            self.assertLess(len(set(in_bag)), 2000)
            fractions.append(len(oob) / 2000)
        self.assertAlmostEqual(sum(fractions) / len(fractions), 1 / math.e, delta=0.01)

    def test_rejects_bad_n(self):
        with self.assertRaises(ValueError):
            bootstrap_sample(0, random.Random(0))

    def test_vote(self):
        models = [lambda x: "cat", lambda x: "dog", lambda x: "cat"]
        self.assertEqual(bagged_predict(models, [1.0]), "cat")
        self.assertEqual(bagged_predict([lambda x: x[0] > 0, lambda x: x[0] > 5, lambda x: x[0] > 1], [3]), True)

    def test_vote_tie_goes_to_smallest(self):
        self.assertEqual(bagged_predict([lambda x: 2, lambda x: 1], None), 1)
        self.assertEqual(bagged_predict([lambda x: "b", lambda x: "c", lambda x: "b", lambda x: "a", lambda x: "a"], None), "a")

    def test_mean(self):
        self.assertAlmostEqual(bagged_predict([lambda x: 1.0, lambda x: 4.0], None, mode="mean"), 2.5)
        models = [lambda x, k=k: k * x for k in range(1, 5)]
        self.assertAlmostEqual(bagged_predict(models, 2.0, mode="mean"), 5.0)

    def test_rejects_bad_models_or_mode(self):
        with self.assertRaises(ValueError):
            bagged_predict([], [1.0])
        with self.assertRaises(ValueError):
            bagged_predict([lambda x: 1], [1.0], mode="median")


if __name__ == "__main__":
    unittest.main(verbosity=2)
