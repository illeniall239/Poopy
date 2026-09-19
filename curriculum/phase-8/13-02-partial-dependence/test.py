import unittest

import numpy as np

from solution import partial_dependence


def data():
    return np.random.default_rng(0).normal(loc=1.0, size=(500, 3))


class TestPartialDependence(unittest.TestCase):
    def test_small_linear_example(self):
        X = np.array([[0.0, 1.0], [0.0, 3.0]])
        got = partial_dependence(lambda A: 2 * A[:, 0] + A[:, 1], X, 0, [0.0, 1.0, 2.0])
        np.testing.assert_allclose(got, [2.0, 4.0, 6.0], atol=1e-12)

    def test_linear_model_gives_a_line_with_the_weight_as_slope(self):
        X = data()
        w = np.array([3.0, -2.0, 0.5])
        grid = np.linspace(-2, 2, 9)
        got = partial_dependence(lambda A: A @ w + 1.0, X, 1, list(grid))
        rest = X[:, 0].mean() * 3.0 + X[:, 2].mean() * 0.5 + 1.0
        np.testing.assert_allclose(got, rest - 2.0 * grid, atol=1e-9)

    def test_averages_predictions_not_the_row(self):
        X = np.array([[0.0, 1.0], [0.0, 3.0]])
        got = partial_dependence(lambda A: A[:, 0] * A[:, 1] ** 2, X, 0, [1.0, 2.0])
        np.testing.assert_allclose(got, [5.0, 10.0], atol=1e-12)

    def test_nonlinear_model_on_real_rows(self):
        X = data()
        f = lambda A: np.sin(A[:, 0]) + A[:, 1] ** 2 * A[:, 2]
        grid = [-1.0, 0.0, 0.5, 3.0]
        got = partial_dependence(f, X, 0, grid)
        expected = [np.sin(g) + np.mean(X[:, 1] ** 2 * X[:, 2]) for g in grid]
        np.testing.assert_allclose(got, expected, atol=1e-9)

    def test_interaction_hides_behind_a_flat_curve(self):
        rng = np.random.default_rng(2)
        x1 = rng.choice([-1.0, 1.0], size=400)
        X = np.column_stack([rng.normal(size=400), x1 - x1.mean()])
        got = partial_dependence(lambda A: A[:, 0] * A[:, 1], X, 0, [-5.0, 0.0, 5.0])
        np.testing.assert_allclose(got, [0.0, 0.0, 0.0], atol=1e-9)

    def test_does_not_modify_X_and_empty_grid(self):
        X = data()
        before = X.copy()
        got = partial_dependence(lambda A: A.sum(axis=1), X, 2, [10.0, 20.0])
        np.testing.assert_array_equal(X, before)
        self.assertEqual(got.shape, (2,))
        self.assertEqual(partial_dependence(lambda A: A.sum(axis=1), X, 2, []).shape, (0,))

    def test_rejects_bad_input(self):
        X = data()
        with self.assertRaises(ValueError):
            partial_dependence(lambda A: A[:, 0], X, 3, [1.0])
        with self.assertRaises(ValueError):
            partial_dependence(lambda A: A[:, 0], X, -1, [1.0])
        with self.assertRaises(ValueError):
            partial_dependence(lambda A: A, X[:, 0], 0, [1.0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
