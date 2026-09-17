import unittest

from solution import search_rotated

ROTATED = [40, 50, 60, 10, 20, 30]


class TestSearchRotated(unittest.TestCase):
    def test_target_in_the_part_after_the_rotation_point(self):
        self.assertEqual(search_rotated(ROTATED, 20), 4)
        self.assertEqual(search_rotated(ROTATED, 10), 3)

    def test_target_in_the_part_before_the_rotation_point(self):
        self.assertEqual(search_rotated(ROTATED, 50), 1)
        self.assertEqual(search_rotated(ROTATED, 40), 0)
        self.assertEqual(search_rotated(ROTATED, 60), 2)

    def test_missing_target(self):
        self.assertEqual(search_rotated(ROTATED, 35), -1)
        self.assertEqual(search_rotated(ROTATED, 5), -1)
        self.assertEqual(search_rotated(ROTATED, 70), -1)

    def test_not_rotated_at_all(self):
        self.assertEqual(search_rotated([10, 20, 30, 40], 30), 2)
        self.assertEqual(search_rotated([10, 20, 30, 40], 25), -1)

    def test_rotated_by_one_in_each_direction(self):
        self.assertEqual(search_rotated([2, 3, 4, 5, 1], 1), 4)
        self.assertEqual(search_rotated([5, 1, 2, 3, 4], 5), 0)
        self.assertEqual(search_rotated([5, 1, 2, 3, 4], 4), 4)

    def test_one_and_two_elements(self):
        self.assertEqual(search_rotated([7], 7), 0)
        self.assertEqual(search_rotated([7], 8), -1)
        self.assertEqual(search_rotated([3, 1], 1), 1)
        self.assertEqual(search_rotated([3, 1], 3), 0)
        self.assertEqual(search_rotated([3, 1], 2), -1)

    def test_empty_list(self):
        self.assertEqual(search_rotated([], 7), -1)

    def test_every_element_of_every_rotation_of_a_small_list(self):
        base = [-9, -4, 0, 3, 8, 15, 21]
        wrong = 0
        for k in range(len(base)):
            nums = base[len(base) - k:] + base[:len(base) - k]
            for i, v in enumerate(nums):
                if search_rotated(nums, v) != i:
                    wrong += 1
                if search_rotated(nums, v + 1) != -1:
                    wrong += 1
        self.assertEqual(wrong, 0)

    def test_20000_searches_in_1000000_rotated_values_in_log_time(self):
        n = 1000000
        k = 300000
        nums = [2 * ((j + k) % n) for j in range(n)]
        wrong = 0
        for q in range(20000):
            i = (q * 7919) % n
            if search_rotated(nums, 2 * i) != (i - k) % n:
                wrong += 1
            if search_rotated(nums, 2 * i + 1) != -1:
                wrong += 1
        self.assertEqual(wrong, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
