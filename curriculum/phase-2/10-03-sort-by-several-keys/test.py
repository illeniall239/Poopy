import unittest

from solution import Player, sort_by_several_keys


def ids_of(players):
    return [p.id for p in players]


class TestSortBySeveralKeys(unittest.TestCase):
    def test_score_descending_then_name_ascending(self):
        players = [Player(1, "cara", 50), Player(2, "alex", 80), Player(3, "bea", 50)]
        self.assertEqual(ids_of(sort_by_several_keys(players)), [2, 3, 1])

    def test_names_only_matter_within_equal_scores(self):
        players = [Player(1, "zed", 90), Player(2, "amy", 70), Player(3, "bob", 90), Player(4, "cat", 70)]
        self.assertEqual(ids_of(sort_by_several_keys(players)), [3, 1, 2, 4])

    def test_fully_equal_keys_keep_their_input_order(self):
        players = [Player(1, "sam", 10), Player(2, "sam", 10), Player(3, "sam", 10)]
        self.assertEqual(ids_of(sort_by_several_keys(players)), [1, 2, 3])
        mixed = [Player(5, "kim", 10), Player(6, "kim", 20), Player(7, "kim", 10)]
        self.assertEqual(ids_of(sort_by_several_keys(mixed)), [6, 5, 7])

    def test_names_compare_by_code_point_upper_case_first(self):
        players = [Player(1, "alice", 5), Player(2, "Bob", 5), Player(3, "aaron", 5)]
        self.assertEqual(ids_of(sort_by_several_keys(players)), [2, 3, 1])

    def test_negative_and_large_scores(self):
        players = [Player(1, "a", -1000000000), Player(2, "b", 1000000000), Player(3, "c", 0)]
        self.assertEqual(ids_of(sort_by_several_keys(players)), [2, 3, 1])

    def test_empty_and_single_element_lists(self):
        self.assertEqual(sort_by_several_keys([]), [])
        self.assertEqual(ids_of(sort_by_several_keys([Player(9, "solo", 1)])), [9])

    def test_returns_the_same_objects_in_a_new_list_and_leaves_the_input_untouched(self):
        players = [Player(1, "b", 1), Player(2, "a", 2)]
        result = sort_by_several_keys(players)
        self.assertIsNot(result, players)
        self.assertIs(result[0], players[1])
        self.assertIs(result[1], players[0])
        self.assertEqual(ids_of(players), [1, 2])

    def test_200000_records_in_o_n_log_n(self):
        n = 200000
        players = [Player(i, "p" + str((i * 7919) % 1000), (i * 104729) % 500) for i in range(n)]
        result = sort_by_several_keys(players)
        self.assertEqual(len(result), n)
        self.assertEqual(len(set(ids_of(result))), n)
        for i in range(1, n):
            a, b = result[i - 1], result[i]
            ordered = a.score > b.score or (a.score == b.score and (a.name < b.name or (a.name == b.name and a.id < b.id)))
            self.assertTrue(ordered, f"records {i - 1} and {i} are out of order")


if __name__ == "__main__":
    unittest.main(verbosity=2)
