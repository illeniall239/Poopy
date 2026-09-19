import math
import unittest

from solution import predict_rating


def ratings():
    return {
        "ann": {"a": 5, "b": 3, "c": 4},
        "bob": {"a": 4, "b": 2, "d": 2},
        "bea": {"a": 4, "b": 2, "d": 4},
        "cat": {"a": 1, "b": 5, "c": 1, "d": 5},
        "dan": {"c": 2, "d": 3},
        "eve": {"a": 3},
        "fay": {"e": 1},
    }


SIM_BOB = 26 / (math.sqrt(34) * math.sqrt(20))  # ann vs bob (and bea) on {a, b}
SIM_CAT = 24 / (math.sqrt(50) * math.sqrt(27))  # ann vs cat on {a, b, c}


class TestUserBasedCF(unittest.TestCase):
    def test_single_shared_item_gives_similarity_one(self):
        self.assertAlmostEqual(predict_rating(ratings(), "ann", "d", 1), 3.0, places=9)

    def test_ties_break_by_user_id(self):
        expected = (1.0 * 3 + SIM_BOB * 4) / (1.0 + SIM_BOB)  # bea, not bob
        self.assertAlmostEqual(predict_rating(ratings(), "ann", "d", 2), expected, places=9)

    def test_cosine_over_co_rated_items_only(self):
        # Every neighbour who rated "d". Filling missing ratings with 0 gives about 2.83 instead.
        expected = (1.0 * 3 + SIM_BOB * 4 + SIM_BOB * 2 + SIM_CAT * 5) / (1.0 + 2 * SIM_BOB + SIM_CAT)
        self.assertAlmostEqual(predict_rating(ratings(), "ann", "d", 10), expected, places=9)

    def test_k_limits_the_neighbours(self):
        expected = (1.0 * 3 + SIM_BOB * 4 + SIM_BOB * 2) / (1.0 + 2 * SIM_BOB)
        self.assertAlmostEqual(predict_rating(ratings(), "ann", "d", 3), expected, places=9)

    def test_fallback_to_the_users_mean(self):
        self.assertAlmostEqual(predict_rating(ratings(), "ann", "z", 3), 4.0, places=9)
        # fay rated "e" but shares no item with ann, so she is not a neighbour.
        self.assertAlmostEqual(predict_rating(ratings(), "ann", "e", 3), 4.0, places=9)

    def test_new_user_does_not_crash(self):
        self.assertAlmostEqual(predict_rating(ratings(), "zed", "d", 3), 3.5, places=9)
        r = ratings()
        r["new"] = {}
        self.assertAlmostEqual(predict_rating(r, "new", "c", 3), 7 / 3, places=9)
        all_values = [v for row in ratings().values() for v in row.values()]
        self.assertAlmostEqual(predict_rating(r, "new", "zzz", 3), sum(all_values) / len(all_values), places=9)

    def test_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            predict_rating(ratings(), "ann", "d", 0)
        with self.assertRaises(ValueError):
            predict_rating({"ann": {}}, "ann", "d", 1)

    def test_does_not_modify_the_ratings(self):
        r = ratings()
        predict_rating(r, "ann", "d", 3)
        predict_rating(r, "zed", "d", 3)
        self.assertEqual(r, ratings())


if __name__ == "__main__":
    unittest.main(verbosity=2)
