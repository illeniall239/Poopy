# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
from dataclasses import dataclass
from typing import Optional


@dataclass(eq=False, repr=False)
class TreeNode:
    val: int
    left: Optional["TreeNode"] = None
    right: Optional["TreeNode"] = None


def _in_range(node: Optional[TreeNode], low: float, high: float) -> bool:
    if node is None:
        return True
    if node.val <= low or node.val >= high:
        return False
    return _in_range(node.left, low, node.val) and _in_range(node.right, node.val, high)


def is_valid_bst(root: Optional[TreeNode]) -> bool:
    return _in_range(root, float("-inf"), float("inf"))
