# Decision tree

Topic: 11. Decision trees
Difficulty: 2 of 3

## Problem

Grow a whole classification tree from greedy splits, in pure Python. Write two functions:

- `build_tree(X: list[list[float]], y: list, max_depth: int | None = None, min_samples: int = 2) -> dict` grows the tree recursively from the root (depth 0).
- `predict_tree(tree: dict, x: list[float])` walks one row `x` from the root to a leaf and returns that leaf's label.

The tree is nested dicts in exactly this shape (the tests read it):

- a leaf: `{"value": label}`
- a split node: `{"feature": int, "threshold": float, "left": subtree, "right": subtree}`, where rows with `x[feature] <= threshold` go left.

At each node, in this order:

1. If `max_depth` is not `None` and the node's depth equals `max_depth`, make a leaf.
2. If the node has fewer than `min_samples` rows, make a leaf.
3. Otherwise find the best split with the rules of exercise `11-02` (Gini gain with children weighted by size, midpoint thresholds, ties to the smaller feature then the smaller threshold, no split unless its gain is above `1e-12`). If there is none (a pure node, or rows that no feature can separate), make a leaf. Otherwise split the rows and grow both children at depth + 1.

A leaf's value is the majority label of its rows; a tie goes to the smallest label (labels in one call are all ints or all strings). `max_depth=None` means no depth limit, so the tree grows until every leaf is pure or unsplittable. `max_depth=0` gives a single leaf. Raise `ValueError` if `X` is empty, `len(X) != len(y)`, `max_depth < 0`, or `min_samples < 1`.

Your file must be standalone: include your own `gini` and `best_split` (you may copy them from `11-01` and `11-02`).

## Examples

```
X = [[1.0], [2.0], [3.0], [4.0]];  y = [0, 0, 1, 1]
build_tree(X, y)                          → {"feature": 0, "threshold": 2.5, "left": {"value": 0}, "right": {"value": 1}}
build_tree(X, y, max_depth=0)             → {"value": 0}      2 against 2: the tie goes to the smaller label
predict_tree(build_tree(X, y), [100.0])   → 1                 no extrapolation: the rightmost leaf
build_tree([[1.0], [1.0], [1.0]], ["b", "a", "b"])   → {"value": "b"}   nothing to split on
```

## Constraints

- Pure Python, no numpy. `collections` is allowed.
- `n` ≤ 200 and `d` ≤ 4 in the tests.
- `predict_tree` is O(depth).

## Hints

1. What does a node need to decide before it looks for any split, and which of those checks are cheap enough to do first?
2. The function that grows a node needs to know how deep it is. How does that number get from a parent to its children?
3. After you pick `(feature, threshold)`, how do you hand each child only its own rows and labels, keeping every row paired with its label?
4. On rows whose features are identical but whose labels differ, what does your best-split step return, and what must the node do so the recursion ends?

## Explain-back

- With `max_depth=None` your tree fits the training set perfectly. Why is that not evidence it is a good model, and what would you look at instead?
- What does `max_depth=1` fail to capture on the toy set in the tests, and which side of the bias–variance trade-off is each depth on?
- The training data has `x` between 0 and 10 and the label rises with `x`. What does your tree predict at `x = 50`, and why can a tree never extrapolate a trend?
- Why does a tree not need one-hot encoding for an ordered category such as "small / medium / large" coded as 0, 1, 2?
