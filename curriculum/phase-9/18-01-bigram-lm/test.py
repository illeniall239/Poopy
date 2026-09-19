import math
import unittest

import numpy as np
from numpy.testing import assert_allclose

from solution import bigram_counts, bigram_probs, sample, avg_nll

WORDS = ["emma", "olivia", "ava", "isabella", "sophia", "mia", "amelia", "ella"]


class TestBigramLM(unittest.TestCase):
    def test_counts_include_start_and_end(self):
        c = bigram_counts(["ab", "a"])
        self.assertEqual(c.shape, (27, 27))
        self.assertEqual((c[0, 1], c[1, 2], c[2, 0], c[1, 0]), (2, 1, 1, 1))
        self.assertEqual(int(c.sum()), 5)
        self.assertEqual(int(bigram_counts(WORDS).sum()), sum(len(w) + 1 for w in WORDS))

    def test_counts_reject_other_characters(self):
        for bad in (["Ab"], ["a-b"], ["a.b"]):
            with self.assertRaises(ValueError):
                bigram_counts(bad)

    def test_probs_normalize_rows(self):
        c = bigram_counts(["ab", "a"])
        p = bigram_probs(c)
        self.assertAlmostEqual(p[1, 2], 0.5)
        self.assertAlmostEqual(p[1, 0], 0.5)
        assert_allclose(p[3], np.zeros(27))  # "c" never seen: row stays zero
        smooth = bigram_probs(c, 1.0)
        assert_allclose(smooth.sum(axis=1), np.ones(27))
        self.assertTrue(np.all(smooth > 0))
        self.assertAlmostEqual(smooth[1, 2], 2 / 29)
        self.assertEqual(int(c.sum()), 5)  # counts not modified
        with self.assertRaises(ValueError):
            bigram_probs(c, -0.5)

    def test_avg_nll_is_a_mean_not_a_sum(self):
        p = bigram_probs(bigram_counts(["ab", "a"]))
        nll = avg_nll(["ab", "a"], p)
        self.assertIsInstance(nll, float)
        self.assertAlmostEqual(nll, 2 * math.log(2) / 5, places=12)

    def test_unseen_bigram_needs_smoothing(self):
        c = bigram_counts(["ab", "a"])
        with np.errstate(all="raise"):
            self.assertEqual(avg_nll(["ba"], bigram_probs(c)), math.inf)
        smoothed = avg_nll(["ba"], bigram_probs(c, 1.0))
        expected = -(math.log(1 / 29) + math.log(1 / 28) + math.log(2 / 29)) / 3
        self.assertAlmostEqual(smoothed, expected, places=12)
        with self.assertRaises(ValueError):
            avg_nll([], bigram_probs(c))

    def test_sample_follows_a_deterministic_chain(self):
        p = np.zeros((27, 27))
        p[0, 1] = p[1, 2] = p[2, 0] = 1.0  # . -> a -> b -> .
        self.assertEqual(sample(p, np.random.default_rng(0), 3), ["ab", "ab", "ab"])
        self.assertEqual(sample(p, np.random.default_rng(0), 0), [])

    def test_sample_is_seeded_by_the_given_rng(self):
        p = bigram_probs(bigram_counts(WORDS), 0.1)
        rng = np.random.default_rng(42)
        expected = []
        for _ in range(5):
            chars, ix = [], 0
            while True:
                ix = int(rng.choice(27, p=p[ix]))
                if ix == 0:
                    break
                chars.append(".abcdefghijklmnopqrstuvwxyz"[ix])
            expected.append("".join(chars))
        np.random.seed(123)
        first = sample(p, np.random.default_rng(42), 5)
        np.random.seed(999)
        second = sample(p, np.random.default_rng(42), 5)
        self.assertEqual(first, second)
        self.assertEqual(first, expected)

    def test_trained_model_beats_uniform(self):
        p = bigram_probs(bigram_counts(WORDS), 1.0)
        self.assertLess(avg_nll(WORDS, p), math.log(27))


if __name__ == "__main__":
    unittest.main(verbosity=2)
