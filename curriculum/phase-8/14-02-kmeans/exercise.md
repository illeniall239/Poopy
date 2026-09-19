# k-means

Topic: 14. Clustering: k-means
Difficulty: 2 of 3

## Problem

Put the two Lloyd steps into a loop. Write with NumPy:

```
kmeans(points: np.ndarray, k: int, seed: int, iters: int = 100) -> tuple[np.ndarray, np.ndarray, list[float]]
```

`points` has shape `(n, d)`. The algorithm:

1. **Init.** `rng = np.random.default_rng(seed)`; the starting centroids are the points at `rng.choice(n, size=k, replace=False)`, in that order. (The test replays this call, so use exactly it.)
2. **Loop** at most `iters` times:
   - `labels` = the nearest centroid for each point (squared Euclidean, ties to the smaller index);
   - `new` = the mean of each cluster's points, an empty cluster keeping its current centroid;
   - append the inertia `Σ ‖pointᵢ − new[labelsᵢ]‖²` (a Python `float`) to the history;
   - if `new` equals the current centroids exactly (`np.array_equal`), stop after adopting `new`; otherwise adopt `new` and go on.
3. Return `(centroids, labels, history)`, where `centroids` has shape `(k, d)`, `labels` (shape `(n,)`) is the nearest-centroid assignment for the returned centroids, and `history` has one entry per loop pass.

Every entry of `history` is less than or equal to the one before it. Raise `ValueError` if `points` is not 2-D, `k` is not between 1 and `n`, or `iters < 1`.

Your file must be standalone: include your own `assign` and `update` (you may copy them from `14-01`).

## Examples

```
centers = [[0, 0], [10, 0], [0, 10]]; points = 30 noisy points around each (spread 0.7)
centroids, labels, history = kmeans(points, 3, seed=0)
centroids          → within 0.5 of the three centers (in some order)
history            → [1198.3, 80.7, 80.7]        non-increasing, stops once nothing moves
kmeans(points, 1, 0)[0]      → [points.mean(axis=0)]
kmeans(np.zeros((3, 2)), 4, 0)   → ValueError
```

## Constraints

- NumPy allowed; no scikit-learn.
- `n` ≤ 1 000, `k` ≤ 10, `d` ≤ 5 in the tests.
- With the pinned init, your final centroids match scikit-learn's Lloyd k-means started from the same points within `1e-8`.

## Hints

1. What is the smallest state the loop has to carry from one pass to the next?
2. How do you know the algorithm has converged without a tolerance? What must be true of the labels once the centroids stop moving?
3. The inertia you record uses `labels` from the old centroids and the `new` centroids. Why is that value never larger than the previous pass's?
4. Two starting centroids sit on the same point. What happens to the second one's cluster in the first pass, and what does your `update` do with it?

## Explain-back

- Run your k-means with ten seeds on the same data and the final inertia differs. Why doesn't Lloyd's algorithm find the global optimum, and what do people do about it?
- Your clusters are compared with the dataset's true labels and only match 70%. Is k-means a classifier? What is it optimizing instead?
- Draw data where k-means fails even with the best seed: two concentric rings, or two long thin parallel clusters. Why does it fail there?
- Why must every column be scaled before k-means, and what happens to the clusters when one column is in metres and another in millimetres?
