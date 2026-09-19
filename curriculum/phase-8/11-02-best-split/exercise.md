# Best split

Topic: 11. Decision trees
Difficulty: 2 of 3

## Problem

A tree grows one greedy split at a time. Write `best_split(X: list[list[float]], y: list) -> tuple[int, float, float] | None` in pure Python. `X` is a list of `n` rows with `d` numeric features each, `y` holds the `n` class labels (any hashable values).

A split is a pair `(feature, threshold)`: rows with `row[feature] <= threshold` go left, the rest go right. For each feature, the candidate thresholds are the midpoints between consecutive **distinct** sorted values of that feature (values `[3, 1, 3, 5]` give candidates `2.0` and `4.0`). Never try a threshold equal to a data value, and never try one that sends every row to the same side.

Score a split by its Gini gain:

```
gain = gini(y) − (n_left / n) · gini(y_left) − (n_right / n) · gini(y_right)
```

Each child's impurity is weighted by its share of the rows. Return `(feature, threshold, gain)` for the split with the largest gain. Ties (gains within `1e-12`) go to the smaller feature index, then the smaller threshold. Return `None` when no split has a gain above `1e-12`: a pure `y`, every feature constant, or a single row. Raise `ValueError` if `X` is empty or `len(X) != len(y)`.

Write your own `gini` helper in the same file (you may copy it from `11-01`).

## Examples

```
best_split([[1.0], [2.0], [3.0], [4.0]], [0, 0, 1, 1])        → (0, 2.5, 0.5)
best_split([[1.0], [3.0]], ["a", "b"])                         → (0, 2.0, 0.5)    the midpoint, not 1.0 or 3.0
best_split([[x] for x in range(1, 9)], [0, 0, 0, 0, 1, 1, 0, 0]) → (0, 4.5, 0.125)
best_split([[1.0, 5.0], [2.0, 5.0]], [0, 0])                   → None             pure node
best_split([[1.0, 5.0], [1.0, 5.0]], [0, 1])                   → None             no feature varies
```

## Constraints

- Pure Python, no numpy. `collections` is allowed.
- `n` ≤ 300, `d` ≤ 5; a straightforward O(d · n²) search is fast enough.
- The gain is within `1e-9` of the exact value; the threshold is exact.

## Hints

1. For one feature with sorted distinct values `[1, 3, 5]`, which thresholds give genuinely different splits of the rows, and why is the midpoint a better choice than `3` itself for a value that later lands between 3 and 5?
2. A split that peels off one row into a pure child has a child impurity of 0. Should that 0 count as much as the impurity of the big child? What decides how much each child counts?
3. If you loop features in order and thresholds in increasing order, what comparison (`>` or `>=`) makes the tie rule come out right without extra code?
4. What should the function report when the labels are already pure, and what gain would every split have then?

## Explain-back

- Why are candidate thresholds placed at midpoints between distinct sorted values, and what goes wrong at prediction time if you use the data values themselves?
- On `[0, 0, 0, 0, 1, 1, 0, 0]`, averaging the children's impurities without weights picks the split at 1.5. Why is that split useless, and how does weighting by size fix it?
- This split is the best one available right now. Why does choosing the best split at every node not guarantee the best tree?
- A feature has values 1, 2, …, 1 000 000 and another has only 0 and 1. Does scaling either of them change which split wins? Why do trees not need feature scaling?
