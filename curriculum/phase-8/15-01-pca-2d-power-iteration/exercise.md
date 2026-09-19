# PCA in two components by power iteration

Topic: 15. PCA and dimensionality reduction
Difficulty: 1 of 3

## Problem

The principal components of a dataset are the eigenvectors of its covariance matrix, largest eigenvalue first. You already wrote power iteration with deflation in Phase 7 (`14-02-power-iteration`); now point it at data. Write with NumPy:

```
pca_2d(points: np.ndarray) -> tuple[np.ndarray, np.ndarray]
```

1. Center the data: subtract each column's mean.
2. Form the sample covariance matrix `C = Xcᵀ Xc / (n − 1)` of shape `(d, d)` (the same as `np.cov(points, rowvar=False)`).
3. Find the top eigenpair `(λ₁, v₁)` of `C` by power iteration, then deflate, `C − λ₁ v₁ v₁ᵀ`, and run power iteration again for `(λ₂, v₂)`.
4. Return `(components, variances)`: `components` of shape `(2, d)` with the unit vectors `v₁` and `v₂` as rows, and `variances = np.array([λ₁, λ₂])`, the variance of the data along each component.

Power iteration here must start from a seeded random vector, `np.random.default_rng(0).normal(size=d)`, normalized, and repeat `v = C v / ‖C v‖` until `‖v_new − v‖ < 1e-12` or 10 000 iterations. The eigenvalue is `vᵀ C v`.

Eigenvectors are only defined up to sign: the test compares `|v · u|` to 1 for NumPy's `u`, never `v` itself, so a component pointing the "other way" is correct.

Do not call `np.linalg.eig`, `eigh` or `svd` in your solution. Raise `ValueError` if `points` is not 2-D or has fewer than 2 rows or fewer than 2 columns.

Your file must be standalone: include your own power iteration (you may copy it from Phase 7).

## Examples

```
points = 500 points stretched 5× along (cos 0.6, sin 0.6) and 1× across it
components, variances = pca_2d(points)
components[0]    → ±[0.820, 0.572]      the long axis
variances        → [≈ 22.0, ≈ 0.89]      about 5² and 1² for this sample
pca_2d(points + 100.0)                  → the same components and variances: centering removes the offset
pca_2d(np.zeros(5))                     → ValueError
```

## Constraints

- NumPy allowed, but no `np.linalg.eig`, `eigh` or `svd`; no scikit-learn.
- `n` ≤ 2 000, `d` ≤ 6; the test data has a clear gap between the top three eigenvalues.
- Variances within `1e-6` of `np.linalg.eigh(np.cov(points, rowvar=False))`'s top two, and `|vᵢ · uᵢ| > 1 − 1e-6`.

## Hints

1. Take a cloud centered at `(100, 100)` that is long in some other direction. Without centering, which direction does the matrix `XᵀX` stretch the most, and is that the direction of spread?
2. What shape does `C` have, and why does its size depend on the number of features rather than the number of rows?
3. After you find `v₁`, what eigenvalue does `C − λ₁ v₁ v₁ᵀ` have for `v₁`, and for the other eigenvectors?
4. Your test compares your component to NumPy's and they differ by a factor of −1. What comparison would treat both as the same answer?

## Explain-back

- Why must the data be centered before PCA? What does the top "component" of uncentered data far from the origin point at?
- Your first component flipped sign after you shuffled the rows. Is that a bug? Why is the sign of a principal component arbitrary?
- The first component of a customer table loads heavily on income and spend. Does that make it "the feature that predicts churn"? What does PCA know about the label?
- Why does power iteration need a gap between `λ₁` and `λ₂` to converge quickly, and what would happen with two equal eigenvalues?
