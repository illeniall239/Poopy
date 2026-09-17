# Maximum depth of a binary tree

Topic: 11. Trees
Difficulty: 1 of 3

## Problem

A company's org chart is stored as a binary tree: every node is a person, and each person has at most two direct reports, `left` and `right`. HR wants to know how many layers of management there are.

The starter defines `TreeNode`: each node has a `val`, a `left` and a `right`, each of which is another node or `null`.

Write `maxDepth(root: TreeNode | null): number`. It returns the number of nodes on the longest path from the root down to a leaf, counting both ends. A leaf is a node with no children.

- An empty tree (`null`) has depth `0`; a single node has depth `1`.
- Only the shape matters; the values stored in the nodes are irrelevant.
- Don't change the tree.

## Examples

Trees are written as level-order arrays, the way the tests build them: values top to bottom, left to right, with `null` for a missing child (the children of a `null` are not listed).

```
maxDepth([3, 9, 20, null, null, 15, 7])  → 3      (3 → 20 → 15)
maxDepth([1, null, 2])                   → 2
maxDepth([1])                            → 1
maxDepth([])                             → 0
```

## Constraints

- 0 to 200 000 nodes.
- Required: O(n) time, where n is the number of nodes, and O(h) extra space for the call stack or queue, where h is the height.
- The large test is a balanced tree of 131 071 nodes (65 535 in Python).

## Hints

1. If someone told you the depth of the left subtree and the depth of the right subtree, how would you compute the depth of the whole tree?
2. What is the depth of an empty subtree? How does answering that let the same rule work for leaves and for nodes with only one child?
3. Write down what your function returns for `[1, null, 2]`, one call at a time. Where does the `+ 1` happen?
4. If you'd rather not recurse: could you count levels with a queue instead? How do you know when one level ends and the next begins?

## Explain-back

- What does each recursive call promise to return about its subtree? Why does that make the code for a single node so short?
- What is the time complexity, and what does the space complexity depend on? Compare a balanced tree with a chain where every node has only a right child.
- Some problems count depth in edges instead of nodes. Which single line would change?
- Would a breadth-first version give the same answer? What would it use memory for instead of the call stack?
