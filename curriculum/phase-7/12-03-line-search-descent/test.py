import math
import unittest

from solution import backtracking_step, line_search_descent

F = lambda v: 0.5 * (v[0] ** 2 + 20 * v[1] ** 2)  # noqa: E731
G = lambda v: [v[0], 20 * v[1]]  # noqa: E731


def norm(v):
    return math.sqrt(sum(t * t for t in v))


class TestLineSearchDescent(unittest.TestCase):
    def test_backtracking_examples(self):
        x = [10.0, 1.0]
        self.assertAlmostEqual(backtracking_step(F, x, F(x), G(x)), 0.0625)
        x = [10.0, 0.0]
        self.assertAlmostEqual(backtracking_step(F, x, F(x), G(x)), 1.0)

    def test_armijo_holds_for_returned_alpha(self):
        for x in [[10.0, 1.0], [-3.0, 0.5], [0.1, 2.0]]:
            fx, g = F(x), G(x)
            alpha = backtracking_step(F, x, fx, g)
            trial = [xi - alpha * gi for xi, gi in zip(x, g)]
            self.assertLessEqual(F(trial), fx - 1e-4 * alpha * sum(t * t for t in g) + 1e-12)

    def test_backtracking_errors_and_budget(self):
        x = [1.0]
        with self.assertRaises(ValueError):
            backtracking_step(F, x, 1.0, [1.0], alpha0=0.0)
        with self.assertRaises(ValueError):
            backtracking_step(F, x, 1.0, [1.0], beta=1.0)
        with self.assertRaises(ValueError):
            backtracking_step(F, x, 1.0, [1.0], c=0.0)
        calls = []
        backtracking_step(lambda v: (calls.append(1), 1e9)[1], [1.0], 0.0, [1.0], max_halvings=7)
        self.assertLessEqual(len(calls), 7)

    def test_converges_where_fixed_rate_struggles(self):
        x, steps = line_search_descent(F, G, [10.0, 1.0])
        self.assertLess(norm(x), 1e-5)
        self.assertLess(steps, 200)
        crawl = [10.0, 1.0]
        for _ in range(steps):
            crawl = [a - 0.001 * b for a, b in zip(crawl, G(crawl))]
        self.assertGreater(norm(crawl), 5.0)
        blow = [10.0, 1.0]
        for _ in range(20):
            blow = [a - 0.15 * b for a, b in zip(blow, G(blow))]
        self.assertGreater(abs(blow[1]), 1e3)

    def test_loss_never_increases(self):
        seen = []

        def f(v):
            return F(v)

        def g(v):
            seen.append(F(v))
            return G(v)

        line_search_descent(f, g, [10.0, 1.0])
        self.assertTrue(all(b <= a + 1e-12 for a, b in zip(seen, seen[1:])))

    def test_already_at_minimum_and_input_untouched(self):
        x0 = [0.0, 0.0]
        x, steps = line_search_descent(F, G, x0)
        self.assertEqual(steps, 0)
        self.assertEqual(x, [0.0, 0.0])
        self.assertIsNot(x, x0)
        line_search_descent(F, G, [1.0, 1.0])

    def test_max_steps(self):
        _, steps = line_search_descent(F, G, [10.0, 1.0], max_steps=3)
        self.assertEqual(steps, 3)

    def test_badly_scaled_100_and_rosenbrock(self):
        f100 = lambda v: 0.5 * (v[0] ** 2 + 100 * v[1] ** 2)  # noqa: E731
        g100 = lambda v: [v[0], 100 * v[1]]  # noqa: E731
        x, steps = line_search_descent(f100, g100, [10.0, 1.0], max_steps=2000)
        self.assertLess(norm(x), 1e-5)
        rosen = lambda v: (1 - v[0]) ** 2 + 100 * (v[1] - v[0] ** 2) ** 2  # noqa: E731
        rosen_g = lambda v: [-2 * (1 - v[0]) - 400 * v[0] * (v[1] - v[0] ** 2), 200 * (v[1] - v[0] ** 2)]  # noqa: E731
        x, _ = line_search_descent(rosen, rosen_g, [-1.2, 1.0], tol=1e-4, max_steps=20_000)
        self.assertAlmostEqual(x[0], 1.0, places=3)
        self.assertAlmostEqual(x[1], 1.0, places=3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
