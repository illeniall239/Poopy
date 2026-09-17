import unittest

from solution import count_islands


class TestCountIslands(unittest.TestCase):
    def test_three_islands(self):
        self.assertEqual(count_islands(["11000", "11000", "00100", "00011"]), 3)

    def test_empty_grid(self):
        self.assertEqual(count_islands([]), 0)

    def test_all_water(self):
        self.assertEqual(count_islands(["000", "000"]), 0)

    def test_diagonal_cells_are_not_connected(self):
        self.assertEqual(count_islands(["101", "010", "101"]), 5)

    def test_an_island_that_winds_around_water(self):
        self.assertEqual(count_islands(["10111", "10101", "11101"]), 1)

    def test_single_row(self):
        self.assertEqual(count_islands(["1011011"]), 3)

    def test_25x25_all_land_is_one_island(self):
        self.assertEqual(count_islands(["1" * 25] * 25), 1)

    def test_500x500_grid_in_linear_time(self):
        grid = [
            "".join("1" if r % 2 == 0 and c % 2 == 0 else "0" for c in range(500)) for r in range(500)
        ]
        self.assertEqual(count_islands(grid), 62500)


if __name__ == "__main__":
    unittest.main(verbosity=2)
