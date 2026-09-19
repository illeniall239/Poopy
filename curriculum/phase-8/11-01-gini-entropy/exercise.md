# Gini impurity and entropy

Topic: 11. Decision trees
Difficulty: 1 of 3

## Problem

A decision tree chooses splits by how mixed the labels in a node are. Write two pure-Python functions that measure that mix for a list of class labels (any hashable values: ints, strings):

- `gini(labels: list) -> float` returns the Gini impurity `1 − Σₖ pₖ²`, where `pₖ` is the fraction of labels equal to class `k`.
- `entropy(labels: list) -> float` returns the entropy in bits, `−Σₖ pₖ log₂ pₖ`, summing only over classes that actually occur (so `0 · log 0` never happens).

Both raise `ValueError` on an empty list. A pure node (one class) has impurity `0.0` for both. A uniform mix of `m` classes has Gini `1 − 1/m` and entropy `log₂ m`, the maximum for `m` classes. The order of the labels does not matter.

## Examples

```
gini([1, 1, 1, 1])              → 0.0
gini([0, 1])                    → 0.5
gini(["a", "a", "a", "b"])      → 0.375     1 − (0.75² + 0.25²)
entropy([0, 1])                 → 1.0
entropy([0, 1, 2, 3])           → 2.0
entropy(["a", "a", "a", "b"])   → 0.8113    −(0.75 log₂ 0.75 + 0.25 log₂ 0.25)
entropy([])                     → ValueError
```

## Constraints

- Pure Python: `math` and `collections` are allowed, numpy is not.
- Lists hold at most 100 000 labels; both functions are O(n).
- Results within `1e-9` of the exact values.

## Hints

1. Before any formula, what do you need to know about the labels: their order, or how many of each class there are?
2. Once you have the class proportions, which of them contribute to the sum, and what happens to a class that never appears?
3. Try both measures on `[0, 1]` and on `[0, 0, 0, 0]`. Which values should come out, and which base of logarithm gives the entropy of a fair coin as exactly 1?
4. Where is the earliest point to notice there is nothing to measure, and what would dividing by zero there look like?

## Explain-back

- Why is an impurity of 0 the goal for a leaf, and why is a tree grown until every leaf is pure not automatically a good tree?
- Gini and entropy almost always pick the same split. What shape do both curves have for two classes, and where are they maximal?
- A column of city names has 300 distinct values. Does a tree need it one-hot encoded before it can split on it, and what would impurity say about a split that isolates one city with two rows?
