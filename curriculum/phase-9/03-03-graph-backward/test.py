import math
import random
import unittest

from solution import graph_backward


def evaluate(nodes, leaves, output):
    """Independent recursive evaluator used for numeric gradients."""
    cache = dict(leaves)

    def val(name):
        if name not in cache:
            op, ins = nodes[name]
            xs = [val(i) for i in ins]
            cache[name] = xs[0] + xs[1] if op == "add" else xs[0] * xs[1] if op == "mul" else math.tanh(xs[0])
        return cache[name]

    return val(output)


def numeric_leaf_grads(nodes, leaves, output, h=1e-6):
    out = {}
    for k in leaves:
        up, down = dict(leaves), dict(leaves)
        up[k] += h
        down[k] -= h
        out[k] = (evaluate(nodes, up, output) - evaluate(nodes, down, output)) / (2 * h)
    return out


class TestGraphBackward(unittest.TestCase):
    def assertDictClose(self, got, want, tol=1e-9):
        self.assertEqual(set(got), set(want))
        for k in want:
            self.assertAlmostEqual(got[k], want[k], delta=tol, msg=k)

    def test_square_accumulates_both_uses(self):
        values, grads = graph_backward({"sq": ("mul", ["x", "x"])}, {"x": 3.0}, "sq")
        self.assertDictClose(values, {"x": 3.0, "sq": 9.0})
        self.assertDictClose(grads, {"x": 6.0, "sq": 1.0})

    def test_karpathy_expression_listed_backwards(self):
        nodes = {"L": ("mul", ["d", "f"]), "d": ("add", ["e", "c"]), "e": ("mul", ["a", "b"])}
        leaves = {"a": 2.0, "b": -3.0, "c": 10.0, "f": -2.0}
        values, grads = graph_backward(nodes, leaves, "L")
        self.assertDictClose(values, {"a": 2.0, "b": -3.0, "c": 10.0, "f": -2.0, "e": -6.0, "d": 4.0, "L": -8.0})
        self.assertDictClose(grads, {"a": 6.0, "b": -4.0, "c": -2.0, "f": 4.0, "e": -2.0, "d": -2.0, "L": 1.0})

    def test_fan_out_at_an_intermediate_node(self):
        # L = tanh(m) + m, m = x * w. Listed so that reversed dict order is NOT a valid backward order.
        nodes = {"t": ("tanh", ["m"]), "L": ("add", ["t", "m"]), "m": ("mul", ["x", "w"])}
        leaves = {"x": 0.5, "w": -1.2}
        values, grads = graph_backward(nodes, leaves, "L")
        m = 0.5 * -1.2
        dm = 1.0 + (1.0 - math.tanh(m) ** 2)
        self.assertAlmostEqual(values["L"], math.tanh(m) + m, delta=1e-12)
        self.assertAlmostEqual(grads["m"], dm, delta=1e-12)
        self.assertAlmostEqual(grads["x"], dm * -1.2, delta=1e-12)
        self.assertAlmostEqual(grads["w"], dm * 0.5, delta=1e-12)
        self.assertAlmostEqual(grads["t"], 1.0, delta=1e-12)

    def test_unrelated_names_get_zero_gradient(self):
        nodes = {"a2": ("add", ["a", "a"]), "other": ("tanh", ["b"])}
        values, grads = graph_backward(nodes, {"a": 1.0, "b": 0.3}, "a2")
        self.assertAlmostEqual(values["other"], math.tanh(0.3), delta=1e-12)
        self.assertDictClose(grads, {"a": 2.0, "b": 0.0, "a2": 1.0, "other": 0.0})

    def test_output_can_be_a_leaf(self):
        values, grads = graph_backward({"n": ("mul", ["x", "y"])}, {"x": 2.0, "y": 5.0}, "y")
        self.assertDictClose(grads, {"x": 0.0, "y": 1.0, "n": 0.0})

    def test_random_graphs_match_numeric_gradients(self):
        rng = random.Random(0)
        for trial in range(15):
            leaves = {f"x{i}": rng.uniform(-1.5, 1.5) for i in range(4)}
            names = list(leaves)
            nodes = {}
            for j in range(12):
                op = rng.choice(["add", "mul", "tanh"])
                k = 1 if op == "tanh" else 2
                nodes[f"n{j}"] = (op, [rng.choice(names) for _ in range(k)])
                names.append(f"n{j}")
            output = names[-1]
            items = list(nodes.items())
            rng.shuffle(items)
            _, grads = graph_backward(dict(items), leaves, output)
            want = numeric_leaf_grads(nodes, leaves, output)
            for k in leaves:
                self.assertAlmostEqual(grads[k], want[k], delta=1e-6, msg=f"trial {trial}, {k}")

    def test_bad_graphs_raise(self):
        bad = [
            ({"n": ("sub", ["x", "x"])}, {"x": 1.0}, "n"),
            ({"n": ("mul", ["x"])}, {"x": 1.0}, "n"),
            ({"n": ("tanh", ["x", "x"])}, {"x": 1.0}, "n"),
            ({"n": ("add", ["x", "ghost"])}, {"x": 1.0}, "n"),
            ({"x": ("tanh", ["y"])}, {"x": 1.0, "y": 2.0}, "x"),
            ({"n": ("tanh", ["x"])}, {"x": 1.0}, "missing"),
            ({"p": ("tanh", ["q"]), "q": ("add", ["p", "x"])}, {"x": 1.0}, "p"),
        ]
        for nodes, leaves, output in bad:
            with self.assertRaises(ValueError, msg=repr(nodes)):
                graph_backward(nodes, leaves, output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
