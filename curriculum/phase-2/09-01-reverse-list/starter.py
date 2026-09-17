from dataclasses import dataclass
from typing import Optional


@dataclass(eq=False, repr=False)
class ListNode:
    val: int
    next: Optional["ListNode"] = None


def reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:
    """Reverse the list in place by changing next pointers, and return the new head."""
    raise NotImplementedError
