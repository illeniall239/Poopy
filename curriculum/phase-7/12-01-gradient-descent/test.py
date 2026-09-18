import unittest

from numpy.testing import assert_allclose

from solution import gradient_descent

GRAD_SQUARE = lambda x: [2 * x[0]]  # noqa: E731


class TestGradientDescent(unittest.TestCase):
    def test_trajectory_on_x_squared(self):
        assert_allclose(gradient_descent(GRAD_SQUARE, [1.0], lr=0.1, steps=3), [[1.0], [0.8], [0.64], [0.512]])

    def test_closed_form(self):
        traj = gradient_descent(GRAD_SQUARE, [3.0], lr=0.25, steps=20)
        self.assertEqual(len(traj), 21)
        for k, point in enumerate(traj):
            self.assertAlmostEqual(point[0], 3.0 * 0.5**k, places=9)

    def test_one_step_to_minimum(self):
        assert_allclose(gradient_descent(GRAD_SQUARE, [1.0], lr=0.5, steps=1), [[1.0], [0.0]])

    def test_oscillation_and_divergence(self):
        assert_allclose(gradient_descent(GRAD_SQUARE, [1.0], lr=1.0, steps=3), [[1.0], [-1.0], [1.0], [-1.0]])
        traj = gradient_descent(GRAD_SQUARE, [1.0], lr=1.1, steps=10)
        mags = [abs(p[0]) for p in traj]
        self.assertTrue(all(b > a for a, b in zip(mags, mags[1:])))
        self.assertGreater(mags[-1], 5.0)

    def test_two_dimensional_bowl(self):
        grad2 = lambda x: [2 * x[0], 20 * x[1]]  # noqa: E731
        final = gradient_descent(grad2, [1.0, 1.0], lr=0.05, steps=100)[-1]
        assert_allclose(final, [0.0, 0.0], atol=1e-4)
        self.assertAlmostEqual(final[0], 0.9**100, places=9)

    def test_zero_steps_and_input_untouched(self):
        x0 = [1.0, 2.0]
        traj = gradient_descent(lambda x: [1.0, 1.0], x0, lr=0.1, steps=0)
        self.assertEqual(traj, [[1.0, 2.0]])
        self.assertIsNot(traj[0], x0)
        gradient_descent(lambda x: [1.0, 1.0], x0, lr=0.1, steps=5)
        self.assertEqual(x0, [1.0, 2.0])

    def test_points_are_distinct_objects(self):
        traj = gradient_descent(lambda x: [1.0], [0.0], lr=0.1, steps=4)
        self.assertEqual(len({id(p) for p in traj}), 5)
        assert_allclose(traj, [[0.0], [-0.1], [-0.2], [-0.3], [-0.4]], atol=1e-12)

    def test_errors_and_call_count(self):
        with self.assertRaises(ValueError):
            gradient_descent(GRAD_SQUARE, [1.0], lr=0.0, steps=1)
        with self.assertRaises(ValueError):
            gradient_descent(GRAD_SQUARE, [1.0], lr=0.1, steps=-1)
        calls = []
        gradient_descent(lambda x: (calls.append(1), [0.0])[1], [1.0], lr=0.1, steps=7)
        self.assertEqual(len(calls), 7)


if __name__ == "__main__":
    unittest.main(verbosity=2)
