# Pairwise distances

Topic: 1. NumPy arrays and vectorization
Difficulty: 3 of 3

## Problem

Write `pairwise_distances(a: np.ndarray, b: np.ndarray) -> np.ndarray`.

`a` has shape `(n, d)` and `b` has shape `(m, d)`: two sets of points in `d` dimensions. Return an array `D` of shape `(n, m)` where `D[i, j]` is the Euclidean distance between `a[i]` and `b[j]`.

No Python loops of any kind. The function must handle `n = m = 2000`, `d = 3` in well under a second, and agree with a loop version within `1e-5`. Raise `ValueError` if the two inputs have different `d`.

NumPy is allowed (and expected).

## Examples

```
a = np.array([[0.0, 0.0], [1.0, 1.0]])
b = np.array([[3.0, 4.0], [0.0, 0.0], [1.0, 1.0]])
pairwise_distances(a, b)
→ array([[5.        , 0.        , 1.41421356],
         [3.60555128, 1.41421356, 0.        ]])

pairwise_distances(np.zeros((2, 3)), np.zeros((4, 2)))  → ValueError
```

## Constraints

- `n, m >= 1`, `d >= 1`; coordinates are floats with absolute value up to 1000.
- Output shape is exactly `(n, m)` and every entry is `>= 0`.
- Time: no Python-level loop over points; both the broadcasting approach and the `|a|² + |b|² − 2a·b` expansion are acceptable.

## Hints

1. If you reshape `a` to `(n, 1, d)` and `b` to `(1, m, d)`, what shape does `a - b` have, and what does each entry mean?
2. Once you have the differences, which axis do you square-and-sum over to get one number per (i, j) pair?
3. There is a second route: expand `|a − b|² = |a|² + |b|² − 2 a·b`. Which single matrix operation gives every `a[i]·b[j]` at once, and what shapes do the two squared-norm terms need so they broadcast to `(n, m)`?
4. In the expansion route, rounding can make a tiny negative number appear where the true distance is 0. What happens when you take its square root, and how do you guard against it?

## Explain-back

- How much memory does the broadcasting approach allocate for `n = m = 2000`, `d = 3`? What about `d = 512`? When would you switch to the expansion formula?
- Why does the expansion formula lose precision for two nearly identical points, when the broadcasting approach does not?
- Broadcasting "stretched" `a` to shape `(n, m, d)`. Did NumPy copy the data `m` times? What does a stride of 0 mean?
- A loop version with `for i in range(n): for j in range(m):` is O(n·m·d) and so is yours. Why is yours so much faster if the big-O is the same?
