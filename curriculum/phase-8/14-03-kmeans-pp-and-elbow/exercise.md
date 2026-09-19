# k-means++ and the elbow

Topic: 14. Clustering: k-means
Difficulty: 3 of 3

## Problem

Random starting centroids often land two in one cluster and none in another, and Lloyd's algorithm cannot recover. k-means++ spreads them out. Write two functions with NumPy:

- `kmeans_pp_init(points: np.ndarray, k: int, rng: np.random.Generator) -> np.ndarray` returns `k` starting centroids, shape `(k, d)`, each a copy of one row of `points`:
  1. the first index is `rng.integers(n)`;
  2. each next index is drawn with `rng.choice(n, p=D2 / D2.sum())`, where `D2[i]` is the squared distance from point `i` to its nearest already-chosen centroid.

  Use exactly those two calls in that order (the test replays them). Points already chosen have `D2 = 0`, so they are never picked twice. Raise `ValueError` if `points` is not 2-D, `k` is not between 1 and `n`, or `D2` sums to 0 before `k` centroids are chosen (fewer distinct points than `k`).

- `inertia_curve(points: np.ndarray, ks: list[int], seed: int) -> list[float]` returns, for each `k` in `ks` in order, the final inertia of k-means started from `kmeans_pp_init(points, k, np.random.default_rng(seed))` (a **fresh** generator for every `k`) and run with Lloyd's algorithm until the centroids stop changing (at most 100 passes). Inertia is `Σ ‖pointᵢ − nearest centroid‖²` as a Python `float`. Use the same assign and update rules as `14-01`: squared Euclidean distance, ties to the smaller index, an empty cluster keeping its centroid.

Plotting `ks` against the curve gives the elbow plot.

Your file must be standalone: include your own Lloyd loop (you may copy it from `14-02`, dropping its random init).

## Examples

```
points = 3 tight blobs of 30 points around (0, 0), (0, 10), (0, 20)
inertia_curve(points, [1, 2, 3, 4], seed=0)   → [≈ 6 060, ≈ 1 529, ≈ 35, ≈ 31]    the elbow is at k = 3
inertia_curve(points, [1], seed=0)[0]          → Σ ‖pointᵢ − mean‖²
kmeans_pp_init(np.array([[1.0, 1.0]] * 5), 2, np.random.default_rng(0))   → ValueError
```

On nine blobs in a 3 × 3 grid with `k = 9`, Lloyd from k-means++ ends at the best inertia for most seeds, while Lloyd from `k` random points usually gets stuck with a much higher one.

## Constraints

- NumPy allowed; no scikit-learn.
- `n` ≤ 500, `k` ≤ 10 in the tests.
- Each draw is O(n · k); the whole init is O(n · k²) or better.

## Hints

1. After the first centroid is picked, which point would you most like the second centroid to be? Why pick far points with high probability rather than always the farthest one?
2. How do you keep, for every point, its squared distance to the nearest centroid chosen so far, without recomputing distances to all of them from scratch each time?
3. What probability does an already-chosen point get, and why does that guarantee distinct centroids as long as there are enough distinct points?
4. Why does `inertia_curve` need a fresh generator per `k`? What would sharing one generator across the loop do to the result for `k = 4` if you added `k = 2` to `ks`?

## Explain-back

- k-means++ still uses randomness and can still end in a local optimum. What does it improve, and what does running several seeds and keeping the lowest inertia add?
- Inertia always goes down as `k` grows. Why can't you choose `k` by minimizing it, and what are you actually looking for in the elbow plot?
- The elbow curve of your real data bends smoothly with no clear corner. What does that tell you, and what else could you use to pick `k` (silhouette, or the purpose of the clustering)?
- Why does k-means++ choose by squared distance and not by distance, and what would it do with a single extreme outlier?
