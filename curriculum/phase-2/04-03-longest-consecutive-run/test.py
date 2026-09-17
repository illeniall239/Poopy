import unittest

from solution import longest_consecutive_run


class TestLongestConsecutiveRun(unittest.TestCase):
    def test_finds_a_run_among_unrelated_values(self):
        self.assertEqual(longest_consecutive_run([100, 4, 200, 1, 3, 2]), 4)

    def test_run_spread_over_the_whole_list(self):
        self.assertEqual(longest_consecutive_run([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]), 9)

    def test_no_two_values_are_consecutive(self):
        self.assertEqual(longest_consecutive_run([10, 30, 20]), 1)
        self.assertEqual(longest_consecutive_run([5]), 1)

    def test_negative_values(self):
        self.assertEqual(longest_consecutive_run([-1, 0, 1, -3, -2]), 5)

    def test_duplicates_count_once(self):
        self.assertEqual(longest_consecutive_run([1, 2, 2, 3]), 3)
        self.assertEqual(longest_consecutive_run([7, 7, 7]), 1)

    def test_empty_list_gives_0(self):
        self.assertEqual(longest_consecutive_run([]), 0)

    def test_picks_the_longest_of_several_runs(self):
        self.assertEqual(longest_consecutive_run([9, 1, 4, 2, 10, 11, 12, 3, 20]), 4)

    def test_does_not_change_the_input(self):
        values = [3, 1, 2]
        longest_consecutive_run(values)
        self.assertEqual(values, [3, 1, 2])

    def test_30000_shuffled_consecutive_values_in_o_n(self):
        n = 30000
        values = [((i * 7919) % n) - 1000 for i in range(n)]
        self.assertEqual(longest_consecutive_run(values), n)


if __name__ == "__main__":
    unittest.main(verbosity=2)
