# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
from dataclasses import dataclass
from typing import Optional


@dataclass(eq=False, repr=False)
class ListNode:
    val: int
    next: Optional["ListNode"] = None


def middle_node(head: Optional[ListNode]) -> Optional[ListNode]:
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
    return slow


def has_cycle(head: Optional[ListNode]) -> bool:
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False
