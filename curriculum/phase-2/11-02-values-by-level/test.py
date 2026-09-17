import unittest

from solution import TreeNode, values_by_level


def from_level_order(values):
    """Builds a tree from a level-order list; None marks a missing child."""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = [root]
    head = 0
    i = 1
    while i < len(values):
        node = queue[head]
        head += 1
        left = values[i]
        i += 1
        if left is not None:
            node.left = TreeNode(left)
            queue.append(node.left)
        if i < len(values):
            right = values[i]
            i += 1
            if right is not None:
                node.right = TreeNode(right)
                queue.append(node.right)
    return root


def complete_tree(n):
    return from_level_order(list(range(n)))


class TestValuesByLevel(unittest.TestCase):
    def test_three_levels(self):
        self.assertEqual(values_by_level(from_level_order([3, 9, 20, None, None, 15, 7])), [[3], [9, 20], [15, 7]])

    def test_chain_with_one_node_per_level(self):
        self.assertEqual(values_by_level(from_level_order([1, None, 2, 3])), [[1], [2], [3]])

    def test_single_node(self):
        self.assertEqual(values_by_level(from_level_order([1])), [[1]])

    def test_empty_tree(self):
        self.assertEqual(values_by_level(None), [])

    def test_missing_children_leave_no_gaps(self):
        self.assertEqual(
            values_by_level(from_level_order([1, 2, 3, None, 4, 5, None, 6, None, None, 7])),
            [[1], [2, 3], [4, 5], [6, 7]],
        )

    def test_left_to_right_within_a_level(self):
        self.assertEqual(values_by_level(from_level_order([10, 5, 15, 3, 7, 12, 20])), [[10], [5, 15], [3, 7, 12, 20]])

    def test_repeated_values_are_each_listed(self):
        self.assertEqual(values_by_level(from_level_order([1, 1, 1, None, 1])), [[1], [1, 1], [1]])

    def test_balanced_tree_of_65535_nodes_in_linear_time(self):
        levels = values_by_level(complete_tree(65535))
        self.assertEqual(len(levels), 16)
        for d in range(16):
            self.assertEqual(levels[d], list(range(2**d - 1, 2 ** (d + 1) - 1)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
