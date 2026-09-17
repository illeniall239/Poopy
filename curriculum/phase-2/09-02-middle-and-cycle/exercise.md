# Middle node and cycle check

Topic: 9. Linked lists
Difficulty: 2 of 3

## Problem

A playlist is stored as a singly linked list of `ListNode`s (defined in the starter). A "shuffle from the middle" feature needs the middle song, and a corrupted save file can make the last node point back into the list, so the player must check for that before walking it.

Write two functions. Both must use fast and slow pointers, and neither may use a `Set`, `Map`, array or any other structure that grows with the list, and neither may change any node.

`middleNode(head: ListNode | null): ListNode | null`
- Returns the middle node of a list with no cycle (the node object itself, not its value).
- For an even number of nodes there are two middle nodes; return the second one.
- An empty list returns `null`.

`hasCycle(head: ListNode | null): boolean`
- Returns `true` if following `next` from `head` ever reaches a node already visited, and `false` if it reaches `null`.
- A node whose `next` points to itself is a cycle. An empty list has no cycle.

## Examples

```
middleNode(1 → 2 → 3 → 4 → 5)       → the node holding 3
middleNode(1 → 2 → 3 → 4 → 5 → 6)   → the node holding 4
middleNode(9)                       → the node holding 9
middleNode(null)                    → null

hasCycle(1 → 2 → 3 → 4 → back to 2) → true
hasCycle(1 → 2 → 3 → 4)             → false
hasCycle(7 → back to 7)             → true
hasCycle(null)                      → false
```

## Constraints

- A list has 0 to 1000000 nodes.
- Required: O(n) time and O(1) extra space for both functions.
- The large tests use 1000000 nodes.

## Hints

1. Two runners start together; one takes one step at a time, the other takes two. Where is the slow runner when the fast one reaches the end of the track?
2. For `middleNode`, trace lists of 1, 2, 5 and 6 nodes. What exact condition should stop the loop so the slow pointer lands on the second middle node for even lengths?
3. For `hasCycle`, if the track is a loop, can the fast runner ever reach the end? What must eventually happen between the two runners instead?
4. Before you read `fast.next.next`, which things must you already know are not `null`? In what order do you check them?

## Explain-back

- Why does the fast pointer always meet the slow pointer inside a cycle, instead of jumping over it forever?
- Why must your loop check `fast !== null` before `fast.next !== null`? What error does the other order cause?
- What are the time and space complexity of each function? Why would a `Set` of visited nodes break the space requirement?
- Where does the slow pointer stop for 6 nodes, and which line of your code decides first-middle versus second-middle?
