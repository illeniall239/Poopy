# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
from dataclasses import dataclass
from typing import Optional


@dataclass(eq=False, repr=False)
class ListNode:
    val: int
    next: Optional["ListNode"] = None


def reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:
    prev = None
    curr = head
    while curr is not None:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev
