# Solve by Gaussian elimination

Topic: 4. Linear systems, inverse, determinant
Difficulty: 2 of 3

## Problem

Write `solve(a: list[list[float]], b: list[float]) -> list[float]` that returns the `x` with `a @ x == b` for a square matrix `a`, in pure Python (no NumPy).

Use Gaussian elimination with partial pivoting on the augmented matrix `[a | b]` to reach upper-triangular form, then back substitution from the last row up. Raise `ValueError` when:

- `a` is not square or `b` has a different length from `a`, or
- the system is singular: some pivot has absolute value below `1e-12` after choosing the largest available entry.

Do not modify `a` or `b`.

## Examples

```
solve([[2, 0], [0, 4]], [2, 8])                     → [1.0, 2.0]
solve([[1, 1], [1, -1]], [3, 1])                    → [2.0, 1.0]
solve([[0, 1], [1, 0]], [5, 7])                     → [7.0, 5.0]     needs a swap
solve([[2, 1, -1], [-3, -1, 2], [-2, 1, 2]], [8, -11, -3])  → [2.0, 3.0, -1.0]
solve([[1, 2], [2, 4]], [3, 6])                     → ValueError   singular
solve([[1, 2], [3, 4]], [1, 2, 3])                  → ValueError   length mismatch
```

## Constraints

- `n` from 1 to 40.
- Must match `numpy.linalg.solve` within `1e-8` on well-conditioned random systems.
- Return a list of `float`s of length `n`.

## Hints

1. Attach `b` as an extra column of each row before eliminating. Why does that make the row operations automatically apply to `b`?
2. After elimination the last row has a single unknown. Which order lets every later row reuse the values already found?
3. The pivot at column `j` is the largest absolute entry in rows `j..n-1` of that column. What goes wrong with `[[0, 1], [1, 0]]` if you never swap?
4. When the largest available pivot is (nearly) zero, what does that say about the columns of `a` and about how many solutions exist?

## Explain-back

- `np.linalg.inv(a) @ b` and `np.linalg.solve(a, b)` give the same `x` mathematically. Why is the second preferred, both for accuracy and for cost?
- A singular system has either no solution or infinitely many. Give a `2×2` example of each and say which column picture matches.
- In least squares you solve `(XᵀX) w = Xᵀy`. What about `X` makes `XᵀX` singular, and what would your function do?
- Elimination on the augmented matrix is O(n³) and back substitution is O(n²). If you must solve for 1000 different right-hand sides with the same `a`, what work can be shared?
