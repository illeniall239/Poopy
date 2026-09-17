import unittest

from solution import days_to_escape


class TestDaysToEscape(unittest.TestCase):
    def test_does_not_slide_back_on_the_last_day(self):
        self.assertEqual(days_to_escape(10, 3, 2), 8)

    def test_reaching_exactly_the_top_counts_as_out(self):
        self.assertEqual(days_to_escape(5, 3, 1), 2)

    def test_one_more_metre_needs_one_more_day(self):
        self.assertEqual(days_to_escape(6, 3, 1), 3)

    def test_out_on_day_1_when_one_climb_is_enough(self):
        self.assertEqual(days_to_escape(3, 5, 1), 1)

    def test_never_escapes_when_the_slide_undoes_the_climb(self):
        self.assertEqual(days_to_escape(10, 2, 2), -1)

    def test_escapes_on_day_1_even_if_the_slide_equals_the_climb(self):
        self.assertEqual(days_to_escape(5, 5, 5), 1)

    def test_never_escapes_when_the_slide_is_bigger_than_the_climb(self):
        self.assertEqual(days_to_escape(10, 3, 7), -1)

    def test_no_slide_at_all(self):
        self.assertEqual(days_to_escape(10, 3, 0), 4)

    def test_deep_well_slow_progress(self):
        self.assertEqual(days_to_escape(1000000, 2, 1), 999999)


if __name__ == "__main__":
    unittest.main(verbosity=2)
