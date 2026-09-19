import unittest

from solution import recommend, user_profile


def feats():
    return {
        "a": [1.0, 0.0, 0.0],
        "b": [0.9, 0.1, 0.0],
        "c": [0.0, 1.0, 0.0],
        "d": [0.0, 0.0, 1.0],
        "e": [1.0, 1.0, 0.0],
        "f": [1.0, 1.0, 0.0],
        "g": [0.0, 50.0, 1.0],
    }


PROFILE = [0.95, 0.05, 0.0]


class TestContentBased(unittest.TestCase):
    def test_profile_is_the_mean_of_liked_vectors(self):
        p = user_profile(feats(), ["a", "b"])
        self.assertEqual(len(p), 3)
        for got, want in zip(p, PROFILE):
            self.assertAlmostEqual(got, want, places=9)
        for got, want in zip(user_profile(feats(), ["d"]), [0.0, 0.0, 1.0]):
            self.assertAlmostEqual(got, want, places=9)

    def test_profile_rejects_empty_and_unknown(self):
        with self.assertRaises(ValueError):
            user_profile(feats(), [])
        with self.assertRaises(ValueError):
            user_profile(feats(), ["a", "nope"])

    def test_ranking_with_ties_by_id(self):
        self.assertEqual(recommend(PROFILE, feats(), 3, {"a", "b"}), ["e", "f", "c"])

    def test_cosine_not_dot_product(self):
        # g has a dot product of 2.5 with the profile, e only 1.0; but e points the right way.
        ranked = recommend(PROFILE, feats(), 10, {"a", "b"})
        self.assertEqual(ranked, ["e", "f", "c", "g", "d"])

    def test_excluded_items_never_return_and_n_limits(self):
        ranked = recommend(PROFILE, feats(), 10, {"a", "b", "e"})
        self.assertNotIn("e", ranked)
        self.assertEqual(ranked, ["f", "c", "g", "d"])
        self.assertEqual(recommend(PROFILE, feats(), 0, set()), [])
        self.assertEqual(recommend(PROFILE, feats(), 2, set()), ["a", "b"])

    def test_zero_vector_item_scores_zero(self):
        f = feats()
        f["z"] = [0.0, 0.0, 0.0]
        # d is orthogonal to the profile (0) and ties with z; d sorts first.
        self.assertEqual(recommend(PROFILE, f, 10, {"a", "b"})[-2:], ["d", "z"])

    def test_brand_new_item_can_be_recommended(self):
        f = feats()
        f["new"] = [1.0, 0.02, 0.0]
        self.assertEqual(recommend(user_profile(f, ["a", "b"]), f, 1, {"a", "b"}), ["new"])

    def test_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            recommend([0.0, 0.0, 0.0], feats(), 3, set())
        with self.assertRaises(ValueError):
            recommend(PROFILE, feats(), -1, set())


if __name__ == "__main__":
    unittest.main(verbosity=2)
