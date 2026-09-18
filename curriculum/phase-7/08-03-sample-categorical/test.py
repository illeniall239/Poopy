import random
import unittest

from solution import empirical_frequencies, sample_categorical


class TestSampleCategorical(unittest.TestCase):
    def test_frequencies_near_probabilities(self):
        probs = [0.2, 0.5, 0.3]
        draws = sample_categorical(probs, 10_000, random.Random(0))
        self.assertEqual(len(draws), 10_000)
        freqs = empirical_frequencies(draws, 3)
        for f, p in zip(freqs, probs):
            self.assertAlmostEqual(f, p, delta=0.02)

    def test_indices_in_range(self):
        draws = sample_categorical([0.1] * 10, 2_000, random.Random(3))
        self.assertTrue(all(0 <= d < 10 for d in draws))
        self.assertTrue(all(isinstance(d, int) for d in draws))

    def test_degenerate_distributions(self):
        rng = random.Random(1)
        self.assertEqual(sample_categorical([1.0], 5, rng), [0] * 5)
        self.assertEqual(sample_categorical([0.0, 1.0], 3, rng), [1, 1, 1])
        self.assertEqual(sample_categorical([0.0, 0.0, 1.0, 0.0], 50, rng), [2] * 50)
        self.assertEqual(sample_categorical([0.5, 0.5], 0, rng), [])

    def test_seed_determinism(self):
        a = sample_categorical([0.3, 0.7], 500, random.Random(42))
        b = sample_categorical([0.3, 0.7], 500, random.Random(42))
        c = sample_categorical([0.3, 0.7], 500, random.Random(43))
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)

    def test_one_random_call_per_draw(self):
        class Counting(random.Random):
            calls = 0

            def random(self):
                self.calls += 1
                return super().random()

        rng = Counting(0)
        sample_categorical([0.25, 0.25, 0.5], 123, rng)
        self.assertEqual(rng.calls, 123)

    def test_rejects_bad_probs(self):
        rng = random.Random(0)
        for bad in [[], [0.5, 0.6], [1.2, -0.2], [0.3, 0.3]]:
            with self.assertRaises(ValueError):
                sample_categorical(bad, 10, rng)
        with self.assertRaises(ValueError):
            sample_categorical([1.0], -1, rng)

    def test_float_noise_in_cumulative_sum(self):
        probs = [0.1] * 10  # sums to 0.9999999999999999 in float
        draws = sample_categorical(probs, 5_000, random.Random(7))
        self.assertTrue(all(0 <= d < 10 for d in draws))
        freqs = empirical_frequencies(draws, 10)
        self.assertAlmostEqual(sum(freqs), 1.0)
        self.assertGreater(freqs[9], 0.05)

    def test_empirical_frequencies(self):
        self.assertEqual(empirical_frequencies([0, 1, 1, 2], 3), [0.25, 0.5, 0.25])
        self.assertEqual(empirical_frequencies([], 3), [0.0, 0.0, 0.0])
        self.assertEqual(empirical_frequencies([2, 2], 4), [0.0, 0.0, 1.0, 0.0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
