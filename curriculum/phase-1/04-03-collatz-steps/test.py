import unittest

from solution import collatz_steps


class TestCollatzSteps(unittest.TestCase):
    def test_sequence_from_6(self):
        self.assertEqual(collatz_steps(6), {"steps": 8, "peak": 16})

    def test_1_needs_no_steps_and_its_peak_is_itself(self):
        self.assertEqual(collatz_steps(1), {"steps": 0, "peak": 1})

    def test_2_needs_exactly_one_step(self):
        self.assertEqual(collatz_steps(2), {"steps": 1, "peak": 2})

    def test_the_starting_number_can_be_the_peak(self):
        self.assertEqual(collatz_steps(16), {"steps": 4, "peak": 16})

    def test_odd_start_climbs_before_falling(self):
        self.assertEqual(collatz_steps(7), {"steps": 16, "peak": 52})

    def test_27_takes_a_long_path(self):
        self.assertEqual(collatz_steps(27), {"steps": 111, "peak": 9232})

    def test_large_start(self):
        self.assertEqual(collatz_steps(837799), {"steps": 524, "peak": 2974984576})


if __name__ == "__main__":
    unittest.main(verbosity=2)
