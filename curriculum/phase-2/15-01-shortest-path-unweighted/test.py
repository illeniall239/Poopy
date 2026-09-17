import unittest

from solution import shortest_path


class TestShortestPath(unittest.TestCase):
    def test_takes_the_shorter_way_round_a_cycle(self):
        self.assertEqual(shortest_path(5, [[0, 1], [1, 2], [2, 3], [3, 4], [0, 4]], 0, 3), 2)

    def test_start_equals_end(self):
        self.assertEqual(shortest_path(3, [[0, 1]], 2, 2), 0)

    def test_unreachable_node_gives_minus_1(self):
        self.assertEqual(shortest_path(4, [[0, 1], [2, 3]], 0, 3), -1)

    def test_node_with_no_edges_gives_minus_1(self):
        self.assertEqual(shortest_path(3, [], 0, 2), -1)

    def test_edges_work_in_both_directions(self):
        self.assertEqual(shortest_path(3, [[1, 0], [2, 1]], 0, 2), 2)

    def test_cycles_and_repeated_edges_do_not_loop_forever(self):
        self.assertEqual(shortest_path(4, [[0, 1], [1, 2], [2, 0], [0, 1], [2, 3]], 0, 3), 2)

    def test_several_routes_of_different_lengths(self):
        self.assertEqual(
            shortest_path(6, [[0, 1], [0, 2], [1, 3], [2, 3], [3, 4], [4, 5], [1, 5]], 0, 5), 2
        )

    def test_path_of_100000_nodes_in_linear_time(self):
        n = 100000
        edges = []
        for i in range(n - 1):
            p = (i * 7919) % (n - 1)
            edges.append([p, p + 1] if i % 2 == 0 else [p + 1, p])
        self.assertEqual(shortest_path(n, edges, 0, n - 1), n - 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
