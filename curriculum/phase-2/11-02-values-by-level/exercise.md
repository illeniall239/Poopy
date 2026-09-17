# Values by level

Topic: 11. Trees
Difficulty: 1 of 3

## Problem

A family tree viewer draws one generation per row: the root on the first row, its children on the second, their children on the third, and so on. It needs the values of the tree grouped by row.

The starter defines `TreeNode`: each node has a `val`, a `left` and a `right`, each of which is another node or `null`.

Write `valuesByLevel(root: TreeNode | null): number[][]`. It returns one array per level, from the root level down to the deepest level. Inside a level, values appear from left to right, exactly as the nodes sit in the tree. Missing children simply don't appear; they do not leave gaps.

- An empty tree (`null`) returns `[]`.
- A single node returns `[[val]]`.
- Values may repeat; each node is listed once.
- Don't change the tree.

## Examples

Trees are written as level-order arrays, the way the tests build them: values top to bottom, left to right, with `null` for a missing child (the children of a `null` are not listed).

```
valuesByLevel([3, 9, 20, null, null, 15, 7])  → [[3], [9, 20], [15, 7]]
valuesByLevel([1, null, 2, 3])                → [[1], [2], [3]]
valuesByLevel([1])                            → [[1]]
valuesByLevel([])                             → []
```

## Constraints

- 0 to 200 000 nodes.
- Required: O(n) time. Extra space O(w) for the queue, where w is the widest level, or O(h) for the call stack if you recurse.
- The large test is a balanced tree of 131 071 nodes (65 535 in Python); its widest level has 65 536 nodes, so removing from the front of an array with `shift` on every step is too slow.

## Hints

1. Which traversal visits all nodes at depth 1 before any node at depth 2? What data structure does it use to remember which nodes to visit next?
2. When you start processing a level, everything in the queue belongs to that level and nothing else does. How many nodes is that? What happens to that number as you add children during the loop?
3. If you record the queue's size before the inner loop, what does the inner loop become? Where do the values of one level get collected?
4. Alternatively, with depth-first recursion: if each call knows its depth, where in the result would it put its value? What must you do when the result has no array for that depth yet?

## Explain-back

- Why does taking the queue's length once before the inner loop keep the levels separate? What goes wrong if you check `queue.length` on every iteration instead?
- What is the time complexity, and what does the extra space depend on? Give a tree where the queue is large and one where it stays tiny.
- Why is `shift()` on a JavaScript array a problem here, and what is the cheap replacement?
- Your DFS classmate got the same answer using recursion and a depth parameter. Why does that work for "left to right within a level", and when would it not?
