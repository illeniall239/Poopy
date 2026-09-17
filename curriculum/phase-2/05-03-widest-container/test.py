import unittest

from solution import widest_container


class TestWidestContainer(unittest.TestCase):
    def test_classic_example(self):
        self.assertEqual(widest_container([1, 8, 6, 2, 5, 4, 8, 3, 7]), 49)

    def test_outer_walls_win_despite_a_dip_in_the_middle(self):
        self.assertEqual(widest_container([4, 3, 2, 1, 4]), 16)

    def test_width_beats_height(self):
        self.assertEqual(widest_container([1, 2, 1]), 2)

    def test_two_tall_neighbours_beat_wide_short_walls(self):
        self.assertEqual(widest_container([2, 3, 4, 5, 18, 17, 6]), 17)

    def test_two_walls(self):
        self.assertEqual(widest_container([1, 1]), 1)
        self.assertEqual(widest_container([3, 9]), 3)

    def test_fewer_than_two_walls_give_0(self):
        self.assertEqual(widest_container([]), 0)
        self.assertEqual(widest_container([5]), 0)

    def test_zero_height_walls_hold_nothing(self):
        self.assertEqual(widest_container([0, 0, 0]), 0)
        self.assertEqual(widest_container([0, 4, 0, 4, 0]), 8)

    def test_does_not_change_the_input(self):
        heights = [3, 1, 2]
        widest_container(heights)
        self.assertEqual(heights, [3, 1, 2])

    def test_30000_alternating_walls_in_o_n(self):
        n = 30000
        heights = [1000 if i % 2 == 0 else 1 for i in range(n)]
        self.assertEqual(widest_container(heights), 1000 * (n - 2))


if __name__ == "__main__":
    unittest.main(verbosity=2)
