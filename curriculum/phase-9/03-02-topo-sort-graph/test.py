import random
import unittest

from solution import topo_sort


class TestTopoSort(unittest.TestCase):
    def assertValidOrder(self, graph, order):
        nodes = set(graph) | {v for vs in graph.values() for v in vs}
        self.assertEqual(len(order), len(nodes), msg="every node exactly once")
        self.assertEqual(set(order), nodes)
        pos = {n: i for i, n in enumerate(order)}
        for u, vs in graph.items():
            for v in vs:
                self.assertLess(pos[u], pos[v], msg=f"edge {u} -> {v}")

    def test_small_dag(self):
        g = {"a": ["c"], "b": ["c"], "c": ["d"]}
        self.assertValidOrder(g, topo_sort(g))

    def test_target_only_nodes_and_duplicate_edges(self):
        g = {"x": ["y", "y"]}
        self.assertEqual(topo_sort(g), ["x", "y"])

    def test_trivial_graphs(self):
        self.assertEqual(topo_sort({"solo": []}), ["solo"])
        self.assertEqual(topo_sort({}), [])

    def test_backprop_shaped_graph_with_fan_out(self):
        # L = tanh(x * w + b) * x : x feeds two nodes at different depths
        g = {"x": ["xw", "L"], "w": ["xw"], "xw": ["n"], "b": ["n"], "n": ["t"], "t": ["L"]}
        order = topo_sort(g)
        self.assertValidOrder(g, order)
        self.assertEqual(order[-1], "L")

    def test_insertion_order_does_not_matter(self):
        # keys listed from the output backwards
        g = {"d": [], "c": ["d"], "b": ["c", "d"], "a": ["b"]}
        self.assertEqual(topo_sort(g), ["a", "b", "c", "d"])

    def test_random_dags(self):
        rng = random.Random(0)
        for _ in range(10):
            n = 60
            names = [f"n{i}" for i in range(n)]
            rng.shuffle(names)  # names[i] may only point to names[j] with j > i
            g = {}
            for i in range(n):
                g[names[i]] = [names[j] for j in range(i + 1, n) if rng.random() < 0.1]
            items = list(g.items())
            rng.shuffle(items)
            g = dict(items)
            self.assertValidOrder(g, topo_sort(g))

    def test_long_chain(self):
        g = {f"n{i}": [f"n{i + 1}"] for i in range(400)}
        self.assertEqual(topo_sort(g), [f"n{i}" for i in range(401)])

    def test_cycles_raise(self):
        for g in ({"a": ["b"], "b": ["a"]}, {"a": ["a"]}, {"s": ["a"], "a": ["b"], "b": ["c"], "c": ["a"]}):
            with self.assertRaises(ValueError, msg=repr(g)):
                topo_sort(g)


if __name__ == "__main__":
    unittest.main(verbosity=2)
