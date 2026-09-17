import math
import unittest

from solution import safe_divide, sum_of_quotients

NAN = math.nan
INF = math.inf


class TestSafeDivideResult(unittest.TestCase):
    def test_divides_normally(self):
        self.assertEqual(safe_divide(10, 4), {"ok": True, "value": 2.5})
        self.assertEqual(safe_divide(0, 5), {"ok": True, "value": 0})
        self.assertEqual(safe_divide(-9, 3), {"ok": True, "value": -3})

    def test_dividing_by_zero_is_a_failure_not_inf(self):
        self.assertEqual(safe_divide(1, 0), {"ok": False, "error": "Cannot divide by zero"})
        self.assertEqual(safe_divide(0, 0), {"ok": False, "error": "Cannot divide by zero"})

    def test_non_finite_inputs_are_a_failure(self):
        self.assertEqual(safe_divide(NAN, 2), {"ok": False, "error": "Inputs must be finite numbers"})
        self.assertEqual(safe_divide(1, INF), {"ok": False, "error": "Inputs must be finite numbers"})
        self.assertEqual(safe_divide(-INF, 1), {"ok": False, "error": "Inputs must be finite numbers"})

    def test_the_finite_check_comes_before_the_zero_check(self):
        self.assertEqual(safe_divide(NAN, 0), {"ok": False, "error": "Inputs must be finite numbers"})

    def test_sums_the_quotients_of_all_pairs(self):
        self.assertEqual(sum_of_quotients([{"a": 10, "b": 2}, {"a": 9, "b": 3}]), {"ok": True, "value": 8})

    def test_no_pairs_sums_to_0(self):
        self.assertEqual(sum_of_quotients([]), {"ok": True, "value": 0})

    def test_reports_the_first_failing_pair_with_its_position(self):
        self.assertEqual(
            sum_of_quotients([{"a": 1, "b": 1}, {"a": 5, "b": 0}, {"a": NAN, "b": 1}]),
            {"ok": False, "error": "Pair 2: Cannot divide by zero"},
        )
        self.assertEqual(
            sum_of_quotients([{"a": INF, "b": 1}]),
            {"ok": False, "error": "Pair 1: Inputs must be finite numbers"},
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
