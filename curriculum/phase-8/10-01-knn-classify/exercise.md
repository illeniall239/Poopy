# kNN classification

Topic: 10. k-nearest neighbors
Difficulty: 1 of 3

## Problem

Write `knn_predict(train_X: np.ndarray, train_y: np.ndarray, x: np.ndarray, k: int) -> int` with NumPy. `train_X` has shape `(n, d)`, `train_y` holds `n` integer labels, `x` is one query point of shape `(d,)`. Return the predicted label as a Python `int`.

The rules, all of which the tests check:

1. **Distance** is Euclidean.
2. **Choosing the k neighbors:** order the training points by distance, and break equal distances by the **smaller training index**. Take the first `k`.
3. **Vote:** the label with the most neighbors among the `k` wins.
4. **Vote ties:** among the labels tied for the most votes, pick the one whose **closest member** (among the `k` neighbors) is nearest to `x`. If that is still tied (two labels' closest members are at exactly the same distance), pick the **smallest label**.

Raise `ValueError` if `k < 1` or `k > n`, if `train_X` is not 2-D, if `len(train_y) != n`, or if `x` does not have `d` entries.

## Examples

```
train_X = [[0, 0], [1, 0], [0, 1], [5, 5], [6, 5]], train_y = [0, 0, 0, 1, 1]
knn_predict(train_X, train_y, [0.2, 0.2], 3)   → 0
knn_predict(train_X, train_y, [5.5, 5.0], 1)   → 1
knn_predict(train_X, train_y, [5.5, 5.0], 5)   → 0         majority, even though the query sits on the 1s
train_X = [[0], [2], [3]], train_y = [7, 4, 4]
knn_predict(train_X, train_y, [1.1], 2)       → 4         tie 1–1; label 4's member at 2 is nearer than 7's at 0
train_X = [[-1], [1]], train_y = [9, 3]
knn_predict(train_X, train_y, [0.0], 2)       → 3         tie 1–1 at equal distance: smallest label
knn_predict(train_X, train_y, [0.0], 3)       → ValueError  k > n
```

## Constraints

- NumPy allowed. Compute all `n` distances in one vectorized expression.
- `n` up to 10 000, `d` up to 100.
- Sorting with `np.argsort(..., kind="stable")` keeps equal distances in index order.

## Hints

1. How do you get all `n` distances from `x` at once with broadcasting?
2. Which sort keeps equal distances in their original order, and why does the rule about smaller training index need that?
3. After counting votes, how do you find every label that shares the top count, not just the first one?
4. For each tied label, what is the distance of its closest neighbor? Given the neighbors are already sorted by distance, where in the list is that neighbor?

## Explain-back

- k = 1 gives zero training error. Why is that not evidence the model is good?
- Why does an even k need a tie rule, and why must the rule be deterministic?
- "kNN has no training step, so it is fast." What is wrong with that claim at prediction time?
- One feature is income in dollars and another is age in years. What happens to the distances, and what should you do first?
