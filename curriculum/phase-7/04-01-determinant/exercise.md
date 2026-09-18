# Determinant by elimination

Topic: 4. Linear systems, inverse, determinant
Difficulty: 2 of 3

## Problem

Write `determinant(a: list[list[float]]) -> float` for a square matrix given as a list of rows, in pure Python (no NumPy).

Use Gaussian elimination with partial pivoting: for each column, pick the row (at or below the diagonal) with the largest absolute value in that column, swap it into place, and eliminate the entries below it. The determinant is the product of the pivots, with the sign flipped once per row swap. If a pivot column has no non-zero entry (below `1e-12` in absolute value), the determinant is `0.0`.

Raise `ValueError` if the matrix is not square. Do not modify the input.

## Examples

```
determinant([[2]])                              → 2.0
determinant([[1, 2], [3, 4]])                   → -2.0
determinant([[2, 0, 0], [0, 3, 0], [0, 0, 4]])  → 24.0
determinant([[0, 1], [1, 0]])                   → -1.0     one swap
determinant([[1, 2], [2, 4]])                   → 0.0      rows are dependent
determinant([[1, 2, 3]])                        → ValueError
```

## Constraints

- `n` from 1 to 30.
- Must match `numpy.linalg.det` within `1e-6` relative tolerance, including the sign.
- Pure Python: copy the rows before eliminating so the caller's matrix is untouched.

## Hints

1. Elimination turns the matrix into an upper-triangular one. What is the determinant of a triangular matrix?
2. Each row operation "add a multiple of one row to another" leaves the determinant unchanged. Which operation does change it, and by what factor?
3. Why choose the largest entry in the column as the pivot rather than the first non-zero one? What happens to the multipliers when the pivot is `1e-10`?
4. `[[0, 1], [1, 0]]` needs a swap before its first pivot exists. Work through what your code produces without the sign flip.

## Explain-back

- A matrix has determinant `1e-9`. Is it nearly singular? What if every entry is around `1e-3` and it is `3×3`?
- Why does swapping two rows negate the determinant? What does that say about the "signed volume" reading?
- Elimination without pivoting on `[[1e-17, 1], [1, 1]]`: what multiplier appears and what does the second row become in floating point?
- The cofactor expansion also computes a determinant. Roughly how many operations does it take for `n = 20` compared with elimination?
