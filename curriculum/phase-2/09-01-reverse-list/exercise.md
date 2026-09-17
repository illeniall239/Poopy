# Reverse a linked list

Topic: 9. Linked lists
Difficulty: 1 of 3

## Problem

A music player keeps the play history as a singly linked list, most recent song first. A "play in original order" button needs the list turned around.

The starter defines `ListNode`: each node has a `val` and a `next` that points to the following node, or `null` at the end of the list.

Write `reverseList(head: ListNode | null): ListNode | null`. It reverses the list in place and returns the new head (the node that used to be last).

- Reuse the existing nodes: change their `next` pointers. Don't create new nodes, and don't copy the values into an array.
- An empty list (`null`) returns `null`; a one-node list returns that same node.
- After reversing, the old head's `next` is `null`.
- Work iteratively with O(1) extra space: no recursion, no arrays, no stacks.

## Examples

```
reverseList(1 → 2 → 3 → 4 → 5)  → 5 → 4 → 3 → 2 → 1
reverseList(1 → 2)              → 2 → 1
reverseList(7)                  → 7
reverseList(null)               → null
```

## Constraints

- The list has 0 to 1000000 nodes.
- Required: O(n) time and O(1) extra space.
- The large test has 200000 nodes, so a recursive solution overflows the call stack and walking to the end of the list again for every node is too slow.

## Hints

1. Draw `1 → 2 → 3` on paper. After you are done, which way should the arrow out of node `2` point?
2. Stand on node `2`. If you change its `next` to point back at `1` right now, how do you reach node `3` afterwards? What must you save first?
3. How many variables do you need to hold while you walk the list: one for the node you're on, one for the node behind you, and what else?
4. When the loop ends, which of your variables holds the new head? Trace a one-node list and an empty list to check.

## Explain-back

- In what order do you update your variables inside the loop, and what breaks if you swap two of those lines?
- Why does a recursive reversal use O(n) extra space even though it creates no new nodes?
- What are the time and space complexity of your solution?
- Why do the tests check that the returned nodes are the same objects as the input nodes?
