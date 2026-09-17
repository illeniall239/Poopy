import unittest

from solution import to_clock


class TestToClock(unittest.TestCase):
    def test_zero_seconds_pads_every_part(self):
        self.assertEqual(to_clock(0), "00:00:00")

    def test_seconds_only(self):
        self.assertEqual(to_clock(59), "00:00:59")

    def test_exactly_one_minute(self):
        self.assertEqual(to_clock(60), "00:01:00")

    def test_one_second_before_an_hour(self):
        self.assertEqual(to_clock(3599), "00:59:59")

    def test_exactly_one_hour(self):
        self.assertEqual(to_clock(3600), "01:00:00")

    def test_every_part_has_two_different_digits(self):
        self.assertEqual(to_clock(45296), "12:34:56")

    def test_single_digit_parts_get_a_leading_zero(self):
        self.assertEqual(to_clock(3725), "01:02:05")

    def test_hours_do_not_wrap_at_24(self):
        self.assertEqual(to_clock(90000), "25:00:00")

    def test_largest_allowed_value(self):
        self.assertEqual(to_clock(359999), "99:59:59")


if __name__ == "__main__":
    unittest.main(verbosity=2)
