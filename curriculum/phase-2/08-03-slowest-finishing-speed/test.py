import unittest

from solution import min_shred_speed


class TestMinShredSpeed(unittest.TestCase):
    def test_speed_between_the_smallest_and_largest_stack(self):
        self.assertEqual(min_shred_speed([3, 6, 7, 11], 8), 4)

    def test_one_hour_per_stack_needs_the_largest_stack_as_speed(self):
        self.assertEqual(min_shred_speed([30, 11, 23, 4, 20], 5), 30)

    def test_one_extra_hour_lowers_the_speed(self):
        self.assertEqual(min_shred_speed([30, 11, 23, 4, 20], 6), 23)

    def test_a_partial_last_hour_still_counts_as_an_hour(self):
        self.assertEqual(min_shred_speed([10], 3), 4)
        self.assertEqual(min_shred_speed([10], 5), 2)
        self.assertEqual(min_shred_speed([10], 10), 1)

    def test_plenty_of_time_gives_speed_1(self):
        self.assertEqual(min_shred_speed([5, 5], 1000000000), 1)

    def test_single_one_page_stack(self):
        self.assertEqual(min_shred_speed([1], 1), 1)

    def test_does_not_change_the_input(self):
        stacks = [11, 3, 7]
        min_shred_speed(stacks, 5)
        self.assertEqual(stacks, [11, 3, 7])

    def test_huge_stacks_with_the_answer_far_from_both_ends(self):
        n = 20000
        stacks = [1] * n
        stacks[n // 2] = 1000000000
        self.assertEqual(min_shred_speed(stacks, n + 1), 500000000)
        stacks[0] = 999999999
        self.assertEqual(min_shred_speed(stacks, n + 4), 333333334)


if __name__ == "__main__":
    unittest.main(verbosity=2)
