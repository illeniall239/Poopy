import unittest

from solution import ListNode, has_cycle, middle_node


def nodes_of(values, loop_to=-1):
    """Builds linked nodes holding values; if loop_to >= 0, the last node points back to nodes[loop_to]."""
    nodes = [ListNode(v) for v in values]
    for a, b in zip(nodes, nodes[1:]):
        a.next = b
    if loop_to >= 0:
        nodes[-1].next = nodes[loop_to]
    return nodes


class TestMiddleAndCycle(unittest.TestCase):
    def test_middle_of_an_odd_length_list(self):
        nodes = nodes_of([1, 2, 3, 4, 5])
        self.assertIs(middle_node(nodes[0]), nodes[2])

    def test_middle_of_an_even_length_list_is_the_second_middle_node(self):
        nodes = nodes_of([1, 2, 3, 4, 5, 6])
        self.assertIs(middle_node(nodes[0]), nodes[3])
        two = nodes_of([1, 2])
        self.assertIs(middle_node(two[0]), two[1])

    def test_middle_of_one_node_and_of_an_empty_list(self):
        one = nodes_of([9])
        self.assertIs(middle_node(one[0]), one[0])
        self.assertIsNone(middle_node(None))

    def test_list_ending_in_none_has_no_cycle(self):
        self.assertIs(has_cycle(nodes_of([1, 2, 3, 4])[0]), False)
        self.assertIs(has_cycle(nodes_of([1])[0]), False)
        self.assertIs(has_cycle(None), False)

    def test_last_node_pointing_back_into_the_list_is_a_cycle(self):
        self.assertIs(has_cycle(nodes_of([1, 2, 3, 4], 1)[0]), True)
        self.assertIs(has_cycle(nodes_of([1, 2, 3, 4], 0)[0]), True)
        self.assertIs(has_cycle(nodes_of([1, 2], 1)[0]), True)

    def test_a_node_pointing_to_itself_is_a_cycle(self):
        self.assertIs(has_cycle(nodes_of([7], 0)[0]), True)

    def test_neither_function_changes_the_nodes(self):
        nodes = nodes_of([5, 6, 7, 8], 2)
        has_cycle(nodes[0])
        plain = nodes_of([1, 2, 3])
        middle_node(plain[0])
        self.assertEqual([n.val for n in nodes], [5, 6, 7, 8])
        self.assertTrue(all(n.next is m for n, m in zip(nodes, [nodes[1], nodes[2], nodes[3], nodes[2]])))
        self.assertEqual([n.val for n in plain], [1, 2, 3])
        self.assertTrue(plain[0].next is plain[1] and plain[1].next is plain[2] and plain[2].next is None)

    def test_200000_nodes_in_linear_time(self):
        n = 200000
        nodes = nodes_of(range(1, n + 1))
        self.assertIs(middle_node(nodes[0]), nodes[n // 2])
        self.assertIs(has_cycle(nodes[0]), False)
        nodes[-1].next = nodes[n // 2]
        self.assertIs(has_cycle(nodes[0]), True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
