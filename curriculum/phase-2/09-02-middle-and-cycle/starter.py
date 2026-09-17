from dataclasses import dataclass
from typing import Optional


@dataclass(eq=False, repr=False)
class ListNode:
    val: int
    next: Optional["ListNode"] = None


def middle_node(head: Optional[ListNode]) -> Optional[ListNode]:
    """Return the middle node (the second middle for even lengths), or None for an empty list."""
    raise NotImplementedError


def has_cycle(head: Optional[ListNode]) -> bool:
    """Return True if following next from head ever revisits a node."""
    raise NotImplementedError
