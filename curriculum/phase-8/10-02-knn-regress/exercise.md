# kNN regression

Topic: 10. k-nearest neighbors
Difficulty: 2 of 3

## Problem

Write `knn_regress(train_X: np.ndarray, train_y: np.ndarray, x: np.ndarray, k: int, weighted: bool = False) -> float` with NumPy. `train_X` has shape `(n, d)`, `train_y` holds `n` float targets, `x` is one query of shape `(d,)`. Return a Python `float`.

1. **Neighbors:** Euclidean distance; order by distance, equal distances broken by the smaller training index; take the first `k`.
2. **Unweighted** (`weighted=False`): the plain mean of the `k` neighbors' targets.
3. **Weighted** (`weighted=True`): inverse-distance weighting, `Σ wᵢ yᵢ / Σ wᵢ` with `wᵢ = 1 / dᵢ`, so closer neighbors count more.
4. **Zero-distance guard:** if one or more of the `k` neighbors sits exactly on `x` (distance `0.0`), `1 / 0` is undefined. In weighted mode, return the mean target of just those zero-distance neighbors and ignore the rest (they are infinitely closer).

Raise `ValueError` if `k < 1` or `k > n`, if `train_X` is not 2-D, if `len(train_y) != n`, or if `x` does not have `d` entries. No NumPy divide or invalid warning may be triggered.

## Examples

```
train_X = [[0.0], [1.0], [3.0], [10.0]], train_y = [0.0, 10.0, 30.0, 100.0]
knn_regress(train_X, train_y, [0.5], 2)                  → 5.0      mean of 0 and 10
knn_regress(train_X, train_y, [0.25], 2, weighted=True)  → 2.5      weights 4 and 4/3: (0 + 40/3) / (16/3)
knn_regress(train_X, train_y, [1.0], 3, weighted=True)   → 10.0     sits on a training point
knn_regress(train_X, train_y, [1.0], 3)                  → 13.333   unweighted ignores the guard
knn_regress([[2.0], [2.0], [5.0]], [1.0, 3.0, 9.0], [2.0], 3, weighted=True)   → 2.0   mean of the two exact matches
knn_regress(train_X, train_y, [0.5], 0)                  → ValueError
```

## Constraints

- NumPy allowed, distances vectorized.
- `n` up to 10 000, `d` up to 100.
- Results within `1e-9` of the tests' expected values.

## Hints

1. Which parts of kNN classification carry over unchanged, and which step replaces the vote?
2. With weights `1 / d`, what happens to a neighbor that is twice as far away? What happens as `d` approaches 0?
3. Where exactly in your code must the zero-distance check happen so that `1 / 0` is never evaluated, even inside a NumPy expression?
4. With `k = n` and no weighting, what does kNN regression predict everywhere? What does that say about k and bias?

## Explain-back

- How does k move kNN regression along the bias–variance trade-off? What does the prediction look like at k = 1 and at k = n?
- Why does inverse-distance weighting need a zero-distance rule, and why is "use the exact matches" a sensible one?
- In 1000 dimensions, the nearest and farthest neighbors are at almost the same distance. What does that do to kNN, and to the weights?
- Why must the features be scaled before computing distances, and on which data do you fit the scaler?
