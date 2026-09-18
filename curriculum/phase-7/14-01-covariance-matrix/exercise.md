# Covariance matrix

Topic: 14. Eigenvectors and SVD, just enough for PCA
Difficulty: 1 of 3

## Problem

Write two functions in pure Python (no NumPy):

- `center(rows: list[list[float]]) -> list[list[float]]` — subtract each column's mean from that column; returns a new list of rows of the same shape.
- `covariance_matrix(rows: list[list[float]], ddof: int = 1) -> list[list[float]]` — the `d×d` matrix `C[i][j] = Σₖ (xₖᵢ - x̄ᵢ)(xₖⱼ - x̄ⱼ) / (n - ddof)` for `n` rows with `d` features each. Equivalent to `np.cov(np.array(rows), rowvar=False, ddof=ddof)`.

Both raise `ValueError` if `rows` is empty or the rows have different lengths; `covariance_matrix` also raises if `n - ddof <= 0`.

## Examples

```
rows = [[1, 2], [3, 6], [5, 10]]           second column is twice the first
center(rows)                → [[-2, -4], [0, 0], [2, 4]]
covariance_matrix(rows)     → [[4.0, 8.0], [8.0, 16.0]]       ddof=1
covariance_matrix(rows, 0)  → [[2.667, 5.333], [5.333, 10.667]]
covariance_matrix([[1, 0], [0, 1], [-1, 0], [0, -1]])  → [[0.667, 0.0], [0.0, 0.667]]   uncorrelated
covariance_matrix([[1, 2]])  → ValueError   n - ddof = 0
```

## Constraints

- Up to 2 000 rows and 20 features; O(n d²) is fine.
- Must match `np.cov(..., rowvar=False)` within `1e-9`.
- The result is symmetric and its diagonal holds each column's variance.

## Hints

1. Which comes first, centering or the products? What does `covariance_matrix` compute if you forget to center a column with mean 100?
2. `C[i][j]` is a dot product of two centred columns. Which earlier exercise gives you columns from rows in one line?
3. What is `C[i][i]` in terms of the variance of column `i`? Use that to check your normalizer.
4. Why is `C` symmetric? Does your loop compute `C[i][j]` and `C[j][i]` separately, and could it skip half the work?

## Explain-back

- Someone computes `XᵀX / (n-1)` without centering and calls it the covariance. On data with mean `[100, 100]` what does the result mostly measure?
- What does a large positive `C[0][1]` say about the two features? What does `C[0][1] = 0` not guarantee?
- Why is the covariance matrix the input to PCA? What do its eigenvectors and eigenvalues mean in terms of the data cloud?
- Feature 0 is in metres and feature 1 in millimetres. How does that show up in `C`, and why does PCA on raw covariance then "prefer" feature 1?
