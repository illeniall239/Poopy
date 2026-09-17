import unittest

from solution import find_seat


class TestFindSeat(unittest.TestCase):
    def test_first_seat_is_row_1_column_1(self):
        self.assertEqual(find_seat(1, 10), {"row": 1, "column": 1})

    def test_seat_in_the_middle_of_a_later_row(self):
        self.assertEqual(find_seat(25, 10), {"row": 3, "column": 5})

    def test_last_seat_in_a_row_stays_in_that_row(self):
        self.assertEqual(find_seat(10, 10), {"row": 1, "column": 10})

    def test_seat_after_the_last_seat_starts_the_next_row(self):
        self.assertEqual(find_seat(11, 10), {"row": 2, "column": 1})

    def test_last_seat_of_a_later_row(self):
        self.assertEqual(find_seat(12, 4), {"row": 3, "column": 4})

    def test_one_seat_per_row(self):
        self.assertEqual(find_seat(7, 1), {"row": 7, "column": 1})

    def test_large_seat_number(self):
        self.assertEqual(find_seat(1000000, 999), {"row": 1002, "column": 1})


if __name__ == "__main__":
    unittest.main(verbosity=2)
