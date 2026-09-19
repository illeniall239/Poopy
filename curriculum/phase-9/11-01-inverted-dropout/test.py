import random
import unittest

from solution import dropout


class TestInvertedDropout(unittest.TestCase):
    def test_eval_mode_is_the_identity(self):
        x = [1.0, -2.0, 3.5]
        self.assertEqual(dropout(x, 0.5, random.Random(0), training=False), x)

    def test_eval_mode_does_not_consume_the_rng(self):
        rng = random.Random(7)
        dropout([1.0, 2.0, 3.0], 0.5, rng, training=False)
        self.assertEqual(rng.random(), random.Random(7).random())

    def test_p_zero_is_the_identity_in_training(self):
        self.assertEqual(dropout([1.0, 2.0, 3.0], 0.0, random.Random(0), training=True), [1.0, 2.0, 3.0])

    def test_matches_the_specified_draws(self):
        x = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
        draws = random.Random(3)
        want = [0.0 if draws.random() < 0.25 else v / 0.75 for v in x]
        got = dropout(x, 0.25, random.Random(3), training=True)
        self.assertEqual(len(got), len(want))
        for g, w in zip(got, want):
            self.assertAlmostEqual(g, w)

    def test_survivors_are_scaled_by_one_over_keep_prob(self):
        out = dropout([2.0] * 200, 0.5, random.Random(1), training=True)
        self.assertTrue(all(v == 0.0 or abs(v - 4.0) < 1e-12 for v in out))
        self.assertIn(0.0, out)

    def test_mean_over_seeds_matches_the_input(self):
        x = [1.0, -2.0, 3.0]
        sums = [0.0, 0.0, 0.0]
        n = 2000
        for seed in range(n):
            for i, v in enumerate(dropout(x, 0.3, random.Random(seed), training=True)):
                sums[i] += v
        for s, v in zip(sums, x):
            self.assertAlmostEqual(s / n, v, delta=0.1)

    def test_does_not_mutate_input_and_handles_empty(self):
        x = [1.0, 2.0, 3.0]
        dropout(x, 0.5, random.Random(0), training=True)
        self.assertEqual(x, [1.0, 2.0, 3.0])
        self.assertEqual(dropout([], 0.3, random.Random(0), training=True), [])

    def test_rejects_bad_p(self):
        for p in (1.0, -0.1, 1.5):
            with self.assertRaises(ValueError):
                dropout([1.0], p, random.Random(0), training=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
