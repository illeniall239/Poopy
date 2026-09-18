# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
from dataclasses import dataclass
from typing import Optional


@dataclass(eq=False, repr=False)
class TreeNode:
    val: int
    left: Optional["TreeNode"] = None
    right: Optional["TreeNode"] = None


def values_by_level(root: Optional[TreeNode]) -> list[list[int]]:
    levels: list[list[int]] = []
    current = [root] if root is not None else []
    while current:
        levels.append([node.val for node in current])
        nxt = []
        for node in current:
            if node.left is not None:
                nxt.append(node.left)
            if node.right is not None:
                nxt.append(node.right)
        current = nxt
    return levels
