import math
import unittest

from solution import chain_derivative, compose, intermediates

SQ = (lambda t: t * t, lambda t: 2 * t)
EX = (math.exp, math.exp)
SIN = (math.sin, math.cos)
LOG1P = (math.log1p, lambda t: 1 / (1 + t))
SIG = (lambda t: 1 / (1 + math.exp(-t)), lambda t: (1 / (1 + math.exp(-t))) * (1 - 1 / (1 + math.exp(-t))))


def central(f, x, h=1e-5):
    return (f(x + h) - f(x - h)) / (2 * h)


class TestChainRuleComposed(unittest.TestCase):
    def test_compose(self):
        self.assertAlmostEqual(compose([SQ, EX], 1.5), math.exp(2.25))
        self.assertAlmostEqual(compose([EX, SQ], 1.5), math.exp(1.5) ** 2)
        self.assertAlmostEqual(compose([], 4.0), 4.0)

    def test_intermediates(self):
        vals = intermediates([SQ, EX], 1.5)
        self.assertEqual(len(vals), 3)
        self.assertAlmostEqual(vals[0], 1.5)
        self.assertAlmostEqual(vals[1], 2.25)
        self.assertAlmostEqual(vals[2], math.exp(2.25))
        self.assertEqual(intermediates([], 2.0), [2.0])

    def test_two_function_chains(self):
        self.assertAlmostEqual(chain_derivative([SQ, EX], 1.5), math.exp(2.25) * 3.0, places=9)
        self.assertAlmostEqual(chain_derivative([EX, SQ], 1.5), 2 * math.exp(1.5) * math.exp(1.5), places=9)

    def test_empty_and_single(self):
        self.assertEqual(chain_derivative([], 4.0), 1.0)
        self.assertAlmostEqual(chain_derivative([SIN], 0.7), math.cos(0.7))

    def test_order_matters(self):
        self.assertNotAlmostEqual(chain_derivative([SQ, EX], 1.5), chain_derivative([EX, SQ], 1.5))

    def test_derivative_evaluated_at_inner_point(self):
        # wrong version evaluates every derivative at x: exp'(x)*2x = exp(1.5)*3 instead of exp(2.25)*3
        self.assertAlmostEqual(chain_derivative([SQ, EX], 1.5), central(lambda x: compose([SQ, EX], x), 1.5), places=6)
        self.assertNotAlmostEqual(chain_derivative([SQ, EX], 1.5), math.exp(1.5) * 3.0, places=2)

    def test_matches_numeric_on_long_chains(self):
        chains = [[SIN, SQ, EX], [LOG1P, SQ, SIN, EX], [SIG] * 6, [SQ, LOG1P, SIG, SIN, EX, LOG1P]]
        for chain in chains:
            for x in [0.3, 0.7, 1.1]:
                analytic = chain_derivative(chain, x)
                numeric = central(lambda t, c=chain: compose(c, t), x)
                self.assertAlmostEqual(analytic, numeric, places=6)

    def test_saturating_chain_shrinks(self):
        d = chain_derivative([SIG] * 10, 0.0)
        expected, v = 1.0, 0.0
        for _ in range(10):
            expected *= SIG[1](v)
            v = SIG[0](v)
        self.assertAlmostEqual(d, expected, places=12)
        self.assertLess(d, 1e-6)

    def test_each_function_called_once(self):
        calls = {"f": 0, "fp": 0}

        def f(t):
            calls["f"] += 1
            return t + 1

        def fp(t):
            calls["fp"] += 1
            return 1.0

        chain_derivative([(f, fp)] * 5, 0.0)
        self.assertEqual(calls, {"f": 5, "fp": 5})


if __name__ == "__main__":
    unittest.main(verbosity=2)
