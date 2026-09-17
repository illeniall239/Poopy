from dataclasses import dataclass
from typing import Optional


@dataclass(eq=False, repr=False)
class TreeNode:
    val: int
    left: Optional["TreeNode"] = None
    right: Optional["TreeNode"] = None


def values_by_level(root: Optional[TreeNode]) -> list[list[int]]:
    """One list per level, top to bottom, each left to right; [] for an empty tree."""
    raise NotImplementedError
