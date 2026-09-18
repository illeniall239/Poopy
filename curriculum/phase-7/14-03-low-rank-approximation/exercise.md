# Low-rank approximation with SVD

Topic: 14. Eigenvectors and SVD, just enough for PCA
Difficulty: 2 of 3

## Problem

Write three functions with NumPy (required), using `np.linalg.svd(X, full_matrices=False)` which returns `U`, the singular values `s` (descending) and `Vt` (that is `Vᵀ`, one right singular vector per **row**):

- `low_rank(X: np.ndarray, k: int) -> np.ndarray` — the best rank-`k` approximation `U[:, :k] · diag(s[:k]) · Vt[:k, :]`, same shape as `X`. Raise `ValueError` if `k < 1` or `k > min(X.shape)`.
- `reconstruction_error(X: np.ndarray, k: int) -> float` — the Frobenius norm `‖X - low_rank(X, k)‖_F`. By the Eckart–Young theorem this equals `sqrt(Σ_{i>k} sᵢ²)`, the energy of the dropped singular values; the test checks both agree.
- `explained_variance(X: np.ndarray, k: int) -> float` — center the columns of `X` first, then return `Σ_{i<=k} sᵢ² / Σ sᵢ²` of the centered matrix: the fraction of variance the first `k` principal components keep. Same `k` checks.

## Examples

```
X = np.array([[3, 0], [0, 0.5]], float)
low_rank(X, 1)                 → [[3, 0], [0, 0]]
reconstruction_error(X, 1)     → 0.5
reconstruction_error(X, 2)     → 0.0

X = np.outer([1, 2, 3], [4, 5])            rank 1
reconstruction_error(X, 1)     → 0.0

rows = 200 points on a line plus small noise
explained_variance(rows, 1)    → about 0.99
explained_variance(rows, 2)    → 1.0
low_rank(X, 0)                 → ValueError
```

## Constraints

- `X` up to `500×100`.
- `low_rank(X, min(X.shape))` reproduces `X` within `1e-9`; `reconstruction_error` must match `sqrt(Σ dropped s²)` within `1e-9`; `explained_variance` is in `[0, 1]`, non-decreasing in `k`, and exactly `1.0` at full rank.
- `explained_variance` must match the eigenvalues of the covariance matrix: `sᵢ² / (n - 1)` are `np.cov`'s eigenvalues after centering.

## Hints

1. `Vt[:k, :]` versus `Vt[:, :k]`: which one takes the first `k` right singular vectors? Check the shape of the product before trusting it.
2. `s` is 1-D. What does `U[:, :k] * s[:k]` do via broadcasting, and how does it compare with `U[:, :k] @ np.diag(s[:k])`?
3. `‖X - X_k‖_F² = Σ_{i>k} sᵢ²`: what does that say about how much you lose by dropping the smallest singular values? Compute it both ways on the `[[3, 0], [0, 0.5]]` example.
4. Why must `explained_variance` center before the SVD? What would the top singular vector of uncentered data with mean `[100, 100]` point at?

## Explain-back

- What does `Vt` from `np.linalg.svd` contain, and how do you get the first principal component from it? What is the common mistake?
- Relate the singular values of centered `X` to the eigenvalues of its covariance matrix. Which one grows with `n`?
- `explained_variance(X, 1) = 0.99`: what does that say about the data cloud, and what would you do with the second component?
- Why is the rank-`k` SVD truncation the best rank-`k` approximation in Frobenius norm, and what is the error if you keep every singular value?
