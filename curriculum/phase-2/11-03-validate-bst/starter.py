from dataclasses import dataclass
from typing import Optional


@dataclass(eq=False, repr=False)
class TreeNode:
    val: int
    left: Optional["TreeNode"] = None
    right: Optional["TreeNode"] = None


def is_valid_bst(root: Optional[TreeNode]) -> bool:
    """True if every node is greater than all of its left subtree and less than all of its right subtree."""
    raise NotImplementedError
