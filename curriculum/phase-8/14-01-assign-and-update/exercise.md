# Assign and update

Topic: 14. Clustering: k-means
Difficulty: 1 of 3

## Problem

Lloyd's algorithm for k-means repeats two steps. Write each one with NumPy:

- `assign(points: np.ndarray, centroids: np.ndarray) -> np.ndarray` takes `points` of shape `(n, d)` and `centroids` of shape `(k, d)` and returns an integer array of shape `(n,)`: for each point, the index of the nearest centroid by squared Euclidean distance. A point equally close to several centroids goes to the smallest index. Raise `ValueError` if either array is not 2-D, their `d` differ, or there are no centroids.
- `update(points: np.ndarray, labels: np.ndarray, k: int, old_centroids: np.ndarray) -> np.ndarray` returns a new float array of shape `(k, d)` where row `c` is the mean of the points labelled `c`. A cluster with no points keeps its row from `old_centroids` (a mean of nothing is NaN, and a NaN centroid would poison every later step). Return a new array; do not modify `old_centroids`. Raise `ValueError` if `len(labels) != len(points)`, `old_centroids` is not of shape `(k, d)`, or a label is outside `range(k)`.

## Examples

```
points = np.array([[0.0, 0.0], [1.0, 0.0], [9.0, 9.0], [10.0, 9.0]])
centroids = np.array([[0.0, 1.0], [9.0, 8.0]])
assign(points, centroids)                              → [0, 0, 1, 1]
update(points, np.array([0, 0, 1, 1]), 2, centroids)   → [[0.5, 0.0], [9.5, 9.0]]
assign(np.array([[1.0]]), np.array([[0.0], [2.0]]))     → [0]     tie: the smaller index
update(points, np.array([0, 0, 0, 0]), 2, centroids)   → [[5.0, 4.5], [9.0, 8.0]]   cluster 1 is empty
```

## Constraints

- NumPy allowed; no scikit-learn.
- `n` ≤ 10 000, `k` ≤ 20, `d` ≤ 10: an `(n, k)` distance matrix fits in memory.
- Centroids within `1e-9` of the exact means.

## Hints

1. If you subtract a `(k, d)` array from an `(n, d)` array, the shapes do not line up. What extra axis would make every point meet every centroid?
2. Why is squared distance enough for choosing the nearest centroid, and what does skipping the square root save?
3. How does `np.argmin` break ties, and is that the rule you need?
4. In `update`, what does the mean of an empty set of points come out as in NumPy, and what should happen instead?

## Explain-back

- Why can neither step increase the inertia (the sum of squared distances from each point to its centroid)? Argue it for the assign step and the update step separately.
- One feature is income in dollars and the other is age in years. Which one decides the nearest centroid, and what should you do before clustering?
- Your clusters line up badly with the dataset's class labels. Is k-means broken? What is it actually optimizing?
- Keeping an empty cluster's old centroid is one choice. What else could you do with an empty cluster, and what does each option risk?
