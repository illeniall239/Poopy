import unittest

from solution import ListNode, reverse_list


def nodes_of(values):
    nodes = [ListNode(v) for v in values]
    for a, b in zip(nodes, nodes[1:]):
        a.next = b
    return nodes


def from_list(values):
    nodes = nodes_of(values)
    return nodes[0] if nodes else None


def to_list(head, limit=2000000):
    """Walks at most `limit` nodes so a list that accidentally loops can't hang the test."""
    values = []
    node = head
    while node is not None and len(values) < limit:
        values.append(node.val)
        node = node.next
    return values


class TestReverseList(unittest.TestCase):
    def test_reverses_five_nodes(self):
        self.assertEqual(to_list(reverse_list(from_list([1, 2, 3, 4, 5]))), [5, 4, 3, 2, 1])

    def test_reverses_two_nodes(self):
        self.assertEqual(to_list(reverse_list(from_list([1, 2]))), [2, 1])

    def test_one_node_returns_the_same_node(self):
        node = ListNode(7)
        self.assertIs(reverse_list(node), node)
        self.assertIsNone(node.next)

    def test_empty_list_returns_none(self):
        self.assertIsNone(reverse_list(None))

    def test_repeated_values(self):
        self.assertEqual(to_list(reverse_list(from_list([1, 1, 2, 3, 3]))), [3, 3, 2, 1, 1])

    def test_reuses_the_original_nodes_and_ends_at_the_old_head(self):
        nodes = nodes_of([10, 20, 30, 40])
        node = reverse_list(nodes[0])
        seen = []
        while node is not None and len(seen) < 10:
            seen.append(node)
            node = node.next
        self.assertEqual(len(seen), 4)
        self.assertTrue(all(a is b for a, b in zip(seen, reversed(nodes))), "expected the same node objects in reverse order")
        self.assertIsNone(nodes[0].next)

    def test_200000_nodes_without_recursion_in_linear_time(self):
        n = 200000
        result = to_list(reverse_list(from_list(list(range(n)))), n + 1)
        self.assertEqual(result, list(range(n - 1, -1, -1)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
