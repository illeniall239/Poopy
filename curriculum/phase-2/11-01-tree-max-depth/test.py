import unittest

from solution import TreeNode, max_depth


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


class TestMaxDepth(unittest.TestCase):
    def test_three_levels(self):
        self.assertEqual(max_depth(from_level_order([3, 9, 20, None, None, 15, 7])), 3)

    def test_only_a_right_child(self):
        self.assertEqual(max_depth(from_level_order([1, None, 2])), 2)

    def test_single_node(self):
        self.assertEqual(max_depth(from_level_order([1])), 1)

    def test_empty_tree(self):
        self.assertEqual(max_depth(None), 0)

    def test_left_leaning_chain(self):
        self.assertEqual(max_depth(from_level_order([1, 2, None, 3, None, 4])), 4)

    def test_deeper_on_one_side(self):
        self.assertEqual(max_depth(from_level_order([1, 2, 3, 4, None, None, None, 5, None, 6])), 5)

    def test_values_do_not_matter(self):
        self.assertEqual(max_depth(from_level_order([-7, -7, -7, 0, 0])), 3)

    def test_balanced_tree_of_65535_nodes_in_linear_time(self):
        self.assertEqual(max_depth(complete_tree(65535)), 16)


if __name__ == "__main__":
    unittest.main(verbosity=2)
