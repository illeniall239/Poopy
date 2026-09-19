# Project and reconstruct

Topic: 15. PCA and dimensionality reduction
Difficulty: 2 of 3

## Problem

Compress data to its top `k` principal components and expand it back. Write two functions with NumPy:

- `project(X: np.ndarray, k: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]` returns `(Z, components, mean)`:
  - `mean`: the column means of `X`, shape `(d,)`;
  - `components`: the top `k` principal directions as unit rows, shape `(k, d)`, largest variance first; take them as the first `k` rows of `Vᵀ` from `np.linalg.svd(X − mean, full_matrices=False)`;
  - `Z = (X − mean) @ componentsᵀ`: each row's coordinates along the components, shape `(n, k)`.

  Raise `ValueError` if `X` is not 2-D or `k` is not between 1 and `min(n, d)`.
- `reconstruct(Z: np.ndarray, components: np.ndarray, mean: np.ndarray) -> np.ndarray` returns `Z @ components + mean`, shape `(n, d)`. Raise `ValueError` if `Z` or `components` is not 2-D or the shapes do not fit together (`Z` is `(n, k)`, `components` is `(k, d)`, `mean` is `(d,)`).

Two facts the test checks, which your code must make true:

- At `k = d` (with `n > d`) the round trip is exact: `reconstruct(*project(X, d))` equals `X` within `1e-9`.
- The squared round-trip error, divided by `n − 1`, equals the dropped variance: `Σ (X − X̂)² / (n − 1)` = the sum of the covariance eigenvalues of the components you left out.

The columns of `Z` are uncorrelated, and the sample variance of column `i` is the `i`-th covariance eigenvalue. Each component's sign is arbitrary, so the test compares `Z` column by column up to sign.

## Examples

```
X = np.array([[0.0, 0.0], [2.0, 0.0], [0.0, 1.0], [2.0, 1.0]])
Z, components, mean = project(X, 1)
mean                                → [1.0, 0.5]
components                          → ±[[1.0, 0.0]]
Z                                   → ±[[-1.0], [1.0], [-1.0], [1.0]]
reconstruct(Z, components, mean)    → [[0.0, 0.5], [2.0, 0.5], [0.0, 0.5], [2.0, 0.5]]
    squared error 4 · 0.25 = 1.0, and 1.0 / (4 − 1) = 1/3: the variance of the dropped second column
project(X, 3)                       → ValueError
```

## Constraints

- NumPy allowed; no scikit-learn.
- `n` ≤ 5 000, `d` ≤ 50.
- Everything within `1e-9` of the exact values.

## Hints

1. Which array must you subtract before projecting, and which must you add back after reconstructing? What goes wrong if the two steps disagree?
2. The components are orthonormal rows. What is `components @ componentsᵀ`, and what does that tell you about going to `Z` and back when `k = d`?
3. For `k < d`, the reconstruction is the projection onto a `k`-dimensional plane. In which directions does each reconstructed row lose information?
4. How can you check the dropped-variance fact numerically: which eigenvalues do you add, and what do you divide the squared error by?

## Explain-back

- Why does reconstruction error equal the variance in the dropped components? Use the fact that the components are orthogonal.
- You fit PCA on the training set. On the test set, should you compute a new mean and new components, or reuse the training ones? Why?
- You reduce 100 columns to 10 with PCA before kNN. What might you gain, and what might you lose for the label you care about?
- A colleague reads component 1 as "customer wealth" because it loads on income and house price. What can a component honestly be said to be?
