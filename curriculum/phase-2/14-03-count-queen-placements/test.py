import unittest

from solution import count_queens


class TestCountQueens(unittest.TestCase):
    def test_one_queen_on_a_1x1_board(self):
        self.assertEqual(count_queens(1), 1)

    def test_no_placement_on_a_2x2_board(self):
        self.assertEqual(count_queens(2), 0)

    def test_no_placement_on_a_3x3_board(self):
        self.assertEqual(count_queens(3), 0)

    def test_two_placements_on_a_4x4_board(self):
        self.assertEqual(count_queens(4), 2)

    def test_four_placements_on_a_6x6_board(self):
        self.assertEqual(count_queens(6), 4)

    def test_92_placements_on_an_8x8_board(self):
        self.assertEqual(count_queens(8), 92)

    def test_12x12_board_needs_pruning(self):
        self.assertEqual(count_queens(12), 14200)


if __name__ == "__main__":
    unittest.main(verbosity=2)
