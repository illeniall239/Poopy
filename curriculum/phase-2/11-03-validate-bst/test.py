import unittest

from solution import TreeNode, is_valid_bst


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


def balanced_bst_level_order(n):
    """Level-order values of a balanced BST holding 0..n-1; for n = 2^h - 1 the tree is complete."""
    values = []
    ranges = [(0, n)]
    head = 0
    while head < len(ranges):
        lo, hi = ranges[head]
        head += 1
        if lo >= hi:
            continue
        mid = (lo + hi) // 2
        values.append(mid)
        ranges.append((lo, mid))
        ranges.append((mid + 1, hi))
    return values


class TestIsValidBst(unittest.TestCase):
    def test_small_valid_tree(self):
        self.assertTrue(is_valid_bst(from_level_order([2, 1, 3])))

    def test_right_child_smaller_than_root(self):
        self.assertFalse(is_valid_bst(from_level_order([5, 1, 4, None, None, 3, 6])))

    def test_grandchild_breaks_an_ancestors_bound(self):
        self.assertFalse(is_valid_bst(from_level_order([5, 4, 6, None, None, 3, 7])))

    def test_equal_values_are_not_allowed(self):
        self.assertFalse(is_valid_bst(from_level_order([2, 2, 2])))
        self.assertFalse(is_valid_bst(from_level_order([2, 1, 2])))

    def test_empty_tree_and_single_node_are_valid(self):
        self.assertTrue(is_valid_bst(None))
        self.assertTrue(is_valid_bst(from_level_order([7])))

    def test_extreme_32_bit_values_are_still_valid(self):
        self.assertTrue(is_valid_bst(from_level_order([-2147483648, None, 2147483647])))
        self.assertTrue(is_valid_bst(from_level_order([2147483647, -2147483648])))

    def test_left_descendant_larger_than_the_root(self):
        self.assertTrue(is_valid_bst(from_level_order([3, 1, 5, 0, 2, 4, 6])))
        self.assertFalse(is_valid_bst(from_level_order([3, 1, 5, 0, 4, 2, 6])))

    def test_balanced_valid_tree_of_65535_nodes_in_linear_time(self):
        self.assertTrue(is_valid_bst(from_level_order(balanced_bst_level_order(65535))))

    def test_balanced_tree_of_65535_nodes_with_one_deep_node_out_of_place(self):
        values = balanced_bst_level_order(65535)
        values[-2] = -1  # still smaller than its parent, but it sits in the root's right subtree
        self.assertFalse(is_valid_bst(from_level_order(values)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
