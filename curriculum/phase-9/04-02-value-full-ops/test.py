import math
import random
import unittest

from solution import Value


def numeric_grads(build, xs, h=1e-6):
    out = []
    for i in range(len(xs)):
        up = [Value(x + (h if j == i else 0.0)) for j, x in enumerate(xs)]
        down = [Value(x - (h if j == i else 0.0)) for j, x in enumerate(xs)]
        out.append((build(*up).data - build(*down).data) / (2 * h))
    return out


class TestValueFullOps(unittest.TestCase):
    def check(self, build, xs):
        vs = [Value(x) for x in xs]
        out = build(*vs)
        self.assertIsInstance(out, Value)
        out.backward()
        for i, (v, want) in enumerate(zip(vs, numeric_grads(build, xs))):
            self.assertAlmostEqual(v.grad, want, delta=1e-6, msg=f"input {i} at {xs}")

    def test_forward_values(self):
        a = Value(3.0)
        self.assertAlmostEqual((a ** 2).data, 9.0)
        self.assertAlmostEqual((a ** -1).data, 1 / 3)
        self.assertAlmostEqual(a.exp().data, math.exp(3.0))
        self.assertAlmostEqual(Value(-2.0).relu().data, 0.0)
        self.assertAlmostEqual((-a).data, -3.0)
        self.assertAlmostEqual((a - 5).data, -2.0)
        self.assertAlmostEqual((a / 4).data, 0.75)

    def test_reflected_ops(self):
        a = Value(3.0)
        for expr, want in [(2 + a, 5.0), (2 * a, 6.0), (2 - a, -1.0), (1 / a, 1 / 3), (1.5 - a, -1.5)]:
            self.assertIsInstance(expr, Value)
            self.assertAlmostEqual(expr.data, want)

    def test_each_op_gradient(self):
        cases = [
            (lambda a: a ** 3, [1.7]),
            (lambda a: a ** 0.5, [2.3]),
            (lambda a: a.exp(), [0.4]),
            (lambda a: a.relu() * 3, [1.2]),
            (lambda a: -a, [0.8]),
            (lambda a, b: a - b, [1.0, 2.5]),
            (lambda a, b: a / b, [1.3, -0.7]),
            (lambda a: 2 + a, [0.5]),
            (lambda a: 3 * a, [0.5]),
            (lambda a: 2 - a, [0.5]),
            (lambda a: 8 / a, [2.0]),
            (lambda a: a.tanh(), [0.3]),
        ]
        for build, xs in cases:
            self.check(build, xs)

    def test_reflected_gradients_exact(self):
        a = Value(2.0)
        (8 / a).backward()
        self.assertAlmostEqual(a.grad, -2.0)
        a = Value(2.0)
        (5 - a).backward()
        self.assertAlmostEqual(a.grad, -1.0)
        a = Value(2.0)
        (a / 4).backward()
        self.assertAlmostEqual(a.grad, 0.25)

    def test_self_cancel_and_self_divide(self):
        a = Value(3.0)
        (a - a).backward()
        self.assertAlmostEqual(a.grad, 0.0)
        b = Value(3.0)
        (b / b).backward()
        self.assertAlmostEqual(b.grad, 0.0)
        c = Value(3.0)
        (c * c * c - c).backward()
        self.assertAlmostEqual(c.grad, 26.0)

    def test_relu_derivative(self):
        for x, want in [(-1.0, 0.0), (0.0, 0.0), (2.0, 1.0)]:
            a = Value(x)
            a.relu().backward()
            self.assertEqual(a.grad, want, msg=f"relu' at {x}")

    def test_pow_rejects_value_exponent(self):
        with self.assertRaises(TypeError):
            Value(2.0) ** Value(2.0)

    def test_softmax_like_expression(self):
        # a stable-softmax-shaped expression mixing every op
        def build(a, b, c):
            ea, eb, ec = (a - 1).exp(), (b - 1).exp(), (c - 1).exp()
            p = ea / (ea + eb + ec)
            return -(p ** 2) + (b * c).relu() / 2 - 1 / (1 + a * a) + (3 - c).tanh()

        rng = random.Random(0)
        for _ in range(10):
            self.check(build, [rng.uniform(-1.5, 1.5) for _ in range(3)])


if __name__ == "__main__":
    unittest.main(verbosity=2)
