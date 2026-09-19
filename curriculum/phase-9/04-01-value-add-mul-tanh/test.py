import math
import random
import unittest

from solution import Value


def numeric_grads(build, xs, h=1e-6):
    """Central differences of build(*values).data with respect to each input float."""
    out = []
    for i in range(len(xs)):
        up = [Value(x + (h if j == i else 0.0)) for j, x in enumerate(xs)]
        down = [Value(x - (h if j == i else 0.0)) for j, x in enumerate(xs)]
        out.append((build(*up).data - build(*down).data) / (2 * h))
    return out


def check(testcase, build, xs):
    vs = [Value(x) for x in xs]
    build(*vs).backward()
    for i, (v, want) in enumerate(zip(vs, numeric_grads(build, xs))):
        testcase.assertAlmostEqual(v.grad, want, delta=1e-6, msg=f"input {i}")


class TestValue(unittest.TestCase):
    def test_forward_values_and_fresh_grad(self):
        a, b = Value(2.0), Value(-3.0)
        c = a * b + 1
        self.assertAlmostEqual(c.data, -5.0)
        self.assertEqual(a.grad, 0.0)
        self.assertAlmostEqual((a * 2).data, 4.0)
        self.assertAlmostEqual(Value(0.5).tanh().data, math.tanh(0.5))

    def test_backward_seeds_output_grad_with_one(self):
        a = Value(1.5)
        out = a * 4
        out.backward()
        self.assertEqual(out.grad, 1.0)
        self.assertAlmostEqual(a.grad, 4.0)

    def test_add_self_accumulates(self):
        a = Value(3.0)
        (a + a).backward()
        self.assertAlmostEqual(a.grad, 2.0)

    def test_mul_self_accumulates(self):
        a = Value(3.0)
        (a * a).backward()
        self.assertAlmostEqual(a.grad, 6.0)

    def test_karpathy_neuron(self):
        x1, x2, w1, w2 = Value(2.0), Value(0.0), Value(-3.0), Value(1.0)
        b = Value(6.881373587019543)
        n = x1 * w1 + x2 * w2 + b
        o = n.tanh()
        o.backward()
        self.assertAlmostEqual(o.data, 0.7071067811865476, places=9)
        self.assertAlmostEqual(n.grad, 0.5, places=9)
        self.assertAlmostEqual(x1.grad, -1.5, places=9)
        self.assertAlmostEqual(w1.grad, 1.0, places=9)
        self.assertAlmostEqual(x2.grad, 0.5, places=9)
        self.assertAlmostEqual(w2.grad, 0.0, places=9)
        self.assertAlmostEqual(b.grad, 0.5, places=9)

    def test_fan_out_at_different_depths_needs_topological_order(self):
        # y feeds a deep path and a shallow path; x feeds three places.
        def build(x, w):
            y = (x * w).tanh()
            z = (y * y + x).tanh() * y + x * y
            return z

        check(self, build, [0.7, -0.4])
        check(self, build, [-1.3, 0.9])

    def test_intermediate_grads_are_filled(self):
        a, b = Value(2.0), Value(5.0)
        s = a + b
        p = s * s
        p.backward()
        self.assertAlmostEqual(s.grad, 14.0)
        self.assertAlmostEqual(a.grad, 14.0)
        self.assertAlmostEqual(b.grad, 14.0)

    def test_random_expressions_match_numeric(self):
        rng = random.Random(0)

        def build(a, b, c):
            t = (a * b + c).tanh()
            return (t * a + t * t * 0.5 + b * -2).tanh() * c + t

        for _ in range(10):
            check(self, build, [rng.uniform(-1.5, 1.5) for _ in range(3)])

    def test_unused_values_keep_zero_grad(self):
        a, b, unused = Value(1.0), Value(2.0), Value(3.0)
        _ = unused * a
        (a * b).backward()
        self.assertEqual(unused.grad, 0.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
