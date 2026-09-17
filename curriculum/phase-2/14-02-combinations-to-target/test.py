import unittest

from solution import combinations_to_target


def normalize(combos: list[list[int]]) -> list[list[int]]:
    """Sorts each combination and then the list, so any output order is accepted."""
    return sorted(sorted(c) for c in combos)


class TestCombinationsToTarget(unittest.TestCase):
    def test_one_repeat_and_one_single(self):
        self.assertEqual(normalize(combinations_to_target([2, 3, 6, 7], 7)), [[2, 2, 3], [7]])

    def test_three_combinations(self):
        self.assertEqual(normalize(combinations_to_target([2, 3, 5], 8)), [[2, 2, 2, 2], [2, 3, 3], [3, 5]])

    def test_no_combination_possible(self):
        self.assertEqual(combinations_to_target([2], 1), [])

    def test_same_candidate_many_times(self):
        self.assertEqual(normalize(combinations_to_target([1], 3)), [[1, 1, 1]])

    def test_unsorted_candidates_no_duplicate_combinations(self):
        candidates = [8, 4, 2]
        self.assertEqual(
            normalize(combinations_to_target(candidates, 8)), [[2, 2, 2, 2], [2, 2, 4], [4, 4], [8]]
        )
        self.assertEqual(candidates, [8, 4, 2])

    def test_order_does_not_make_a_new_combination(self):
        self.assertEqual(normalize(combinations_to_target([1, 2], 4)), [[1, 1, 1, 1], [1, 1, 2], [2, 2]])

    def test_531_combinations_for_target_60(self):
        result = normalize(combinations_to_target([2, 3, 5, 7, 11], 60))
        self.assertEqual(len(result), 531)
        self.assertEqual(len({tuple(c) for c in result}), 531)
        for c in result:
            self.assertEqual(sum(c), 60)
            self.assertTrue(all(v in (2, 3, 5, 7, 11) for v in c))


if __name__ == "__main__":
    unittest.main(verbosity=2)
