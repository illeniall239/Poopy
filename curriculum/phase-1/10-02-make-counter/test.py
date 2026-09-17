import unittest

from solution import make_counter


class TestMakeCounter(unittest.TestCase):
    def test_starts_at_0_and_steps_by_1_by_default(self):
        c = make_counter()
        self.assertEqual(c.value(), 0)
        self.assertEqual(c.increment(), 1)
        self.assertEqual(c.increment(), 2)
        self.assertEqual(c.decrement(), 1)
        self.assertEqual(c.value(), 1)

    def test_uses_a_custom_start_and_step(self):
        c = make_counter(100, 10)
        self.assertEqual(c.increment(), 110)
        self.assertEqual(c.decrement(), 100)
        self.assertEqual(c.decrement(), 90)

    def test_reset_goes_back_to_the_start_not_to_0(self):
        c = make_counter(5)
        c.increment()
        c.increment()
        self.assertEqual(c.reset(), 5)
        self.assertEqual(c.value(), 5)

    def test_value_does_not_change_the_count(self):
        c = make_counter(3)
        c.value()
        c.value()
        self.assertEqual(c.increment(), 4)

    def test_counters_are_independent(self):
        a = make_counter()
        b = make_counter()
        a.increment()
        a.increment()
        self.assertEqual(b.increment(), 1)
        self.assertEqual(a.value(), 2)

    def test_functions_still_work_when_taken_off_the_object(self):
        c = make_counter()
        inc = c.increment
        read = c.value
        inc()
        inc()
        self.assertEqual(read(), 2)

    def test_the_count_is_private(self):
        c = make_counter()
        self.assertEqual(sorted(vars(c)), ["decrement", "increment", "reset", "value"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
