# Validate a binary search tree

Topic: 11. Trees
Difficulty: 2 of 3

## Problem

An index was saved to disk as a binary tree and loaded back. Before trusting it for lookups, you must check that it is still a valid binary search tree.

The starter defines `TreeNode`: each node has a `val`, a `left` and a `right`, each of which is another node or `null`.

Write `isValidBst(root: TreeNode | null): boolean`. A tree is a valid binary search tree when, for every node, every value anywhere in its left subtree is strictly less than the node's value, and every value anywhere in its right subtree is strictly greater. The rule applies to the whole subtree, not just the direct children.

- Equal values are not allowed: a node whose child has the same value is invalid.
- An empty tree (`null`) and a single node are valid.
- Node values are 32-bit integers, and the tests include the extremes `-2147483648` and `2147483647` as node values. Your bounds must not be limited to that range.
- Don't change the tree.

## Examples

Trees are written as level-order arrays, the way the tests build them: values top to bottom, left to right, with `null` for a missing child (the children of a `null` are not listed).

```
isValidBst([2, 1, 3])                        → true
isValidBst([5, 1, 4, null, null, 3, 6])      → false    (4 is in the right subtree of 5)
isValidBst([5, 4, 6, null, null, 3, 7])      → false    (3 is a right descendant of 5, yet 3 < 5)
isValidBst([2, 2, 2])                        → false
isValidBst([])                               → true
```

## Constraints

- 0 to 200 000 nodes.
- Required: O(n) time and O(h) extra space, where h is the height.
- The large tests are balanced trees of 131 071 nodes (65 535 in Python), one valid and one with a single deep node out of place.

## Hints

1. In the third example, node `3` is smaller than its parent `6`, so a check that compares each node only with its own children says it's fine. What does the root `5` require of *everything* on its right?
2. Every node sits inside an allowed range: a lower bound and an upper bound inherited from its ancestors. What is the range for the root? How does the range change when you step to a left child? To a right child?
3. What should the initial bounds be so that a node holding the smallest or largest possible integer is still accepted? In your language, what value works?
4. Another route: what order does an inorder traversal of a valid BST produce the values in? What would you compare each visited value against?

## Explain-back

- Why does checking only parent-child pairs fail? Give a tree where every parent-child pair is in order but the tree is not a BST.
- What are the time and space complexity? Why does the space depend on the height rather than the number of nodes?
- How does your solution reject a node equal to an ancestor's value? Which comparison makes it strict?
- Compare the bounds approach with the inorder approach: what does each keep track of, and which would you pick if you also needed to find the first out-of-order value?
