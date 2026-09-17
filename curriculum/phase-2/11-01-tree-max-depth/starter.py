from dataclasses import dataclass
from typing import Optional


@dataclass(eq=False, repr=False)
class TreeNode:
    val: int
    left: Optional["TreeNode"] = None
    right: Optional["TreeNode"] = None


def max_depth(root: Optional[TreeNode]) -> int:
    """Number of nodes on the longest root-to-leaf path; 0 for an empty tree."""
    raise NotImplementedError
