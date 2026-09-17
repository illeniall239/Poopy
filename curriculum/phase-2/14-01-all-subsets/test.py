import unittest

from solution import subsets


def normalize(sets: list[list[int]]) -> list[list[int]]:
    """Sorts each subset and then the list of subsets, so any output order is accepted."""
    return sorted(sorted(s) for s in sets)


def distinct_count(sets: list[list[int]]) -> int:
    return len({tuple(sorted(s)) for s in sets})


class TestSubsets(unittest.TestCase):
    def test_all_subsets_of_three_numbers(self):
        self.assertEqual(
            normalize(subsets([1, 2, 3])),
            normalize([[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]),
        )

    def test_empty_list_has_only_the_empty_subset(self):
        self.assertEqual(subsets([]), [[]])

    def test_one_number(self):
        self.assertEqual(normalize(subsets([5])), [[], [5]])

    def test_negative_and_unsorted_numbers(self):
        self.assertEqual(normalize(subsets([3, -1])), [[], [-1], [-1, 3], [3]])

    def test_each_stored_subset_is_its_own_copy(self):
        nums = [4, 8, 15, 16, 23, 42, -1, -2, -3, 0]
        result = subsets(nums)
        self.assertEqual(len(result), 1024)
        self.assertEqual(distinct_count(result), 1024)
        self.assertEqual(nums, [4, 8, 15, 16, 23, 42, -1, -2, -3, 0])

    def test_all_65536_subsets_of_16_numbers(self):
        nums = [i * 3 - 20 for i in range(16)]
        result = subsets(nums)
        self.assertEqual(len(result), 65536)
        self.assertEqual(distinct_count(result), 65536)


if __name__ == "__main__":
    unittest.main(verbosity=2)
