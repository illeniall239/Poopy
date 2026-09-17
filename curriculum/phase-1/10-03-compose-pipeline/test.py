import unittest

from solution import pipeline, when


def add_one(n):
    return n + 1


def double(n):
    return n * 2


class TestComposePipeline(unittest.TestCase):
    def test_runs_steps_left_to_right(self):
        self.assertEqual(pipeline([add_one, double])(3), 8)
        self.assertEqual(pipeline([double, add_one])(3), 7)

    def test_no_steps_returns_the_input_unchanged(self):
        self.assertEqual(pipeline([])(42), 42)

    def test_each_step_runs_exactly_once_per_call(self):
        calls = []

        def counted(n):
            calls.append(n)
            return n

        pipeline([counted, add_one, counted])(0)
        self.assertEqual(len(calls), 2)

    def test_the_returned_step_can_be_reused(self):
        run = pipeline([add_one, double])
        self.assertEqual(run(1), 4)
        self.assertEqual(run(1), 4)
        self.assertEqual(run(10), 22)

    def test_changing_the_steps_list_afterwards_has_no_effect(self):
        steps = [add_one]
        run = pipeline(steps)
        steps.append(double)
        self.assertEqual(run(5), 6)

    def test_when_runs_the_step_only_if_the_predicate_holds(self):
        halve_evens = when(lambda n: n % 2 == 0, lambda n: n / 2)
        self.assertEqual(halve_evens(10), 5)
        self.assertEqual(halve_evens(7), 7)

    def test_pipelines_and_when_combine(self):
        halve_evens = when(lambda n: n % 2 == 0, lambda n: n / 2)
        self.assertEqual(pipeline([add_one, halve_evens, double])(5), 6)
        self.assertEqual(pipeline([pipeline([add_one, add_one]), double])(1), 6)


if __name__ == "__main__":
    unittest.main(verbosity=2)
