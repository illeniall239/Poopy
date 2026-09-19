# Explained variance ratio

Topic: 15. PCA and dimensionality reduction
Difficulty: 2 of 3

## Problem

How many components should you keep? Look at how much of the data's variance each one carries. Write with NumPy:

```
explained_variance_ratio(X: np.ndarray, k: int) -> np.ndarray
```

1. Center `X` (shape `(n, d)`): subtract each column's mean.
2. Take the singular values `s₁ ≥ s₂ ≥ …` of the centered matrix with `np.linalg.svd`. The variance along component `i` is `sᵢ² / (n − 1)`, the `i`-th eigenvalue of the covariance matrix.
3. Return the first `k` ratios `sᵢ² / Σⱼ sⱼ²` as a float array of shape `(k,)`, largest first.

All `min(n, d)` ratios together sum to 1, so at `k = min(n, d)` the result sums to 1. Every ratio is between 0 and 1. Multiplying all of `X` by a constant or adding a constant to it changes nothing.

Raise `ValueError` if `X` is not 2-D, `k` is not between 1 and `min(n, d)`, or `X` has zero total variance (every row identical).

## Examples

```
X = np.array([[0.0, 0.0], [1.0, 1.0], [2.0, 2.0], [3.0, 3.0]])
explained_variance_ratio(X, 2)       → [1.0, 0.0]         all points on one line
X = np.array([[0.0, 0.0], [2.0, 0.0], [0.0, 1.0], [2.0, 1.0]])
explained_variance_ratio(X, 2)       → [0.8, 0.2]         column variances 4/3 and 1/3
explained_variance_ratio(X + 50, 1)  → [0.8]              the offset does not matter
explained_variance_ratio(X, 3)       → ValueError         only 2 components exist
```

## Constraints

- NumPy allowed; no scikit-learn.
- `n` ≤ 5 000, `d` ≤ 50.
- Ratios within `1e-9` of scikit-learn's `PCA().explained_variance_ratio_`.

## Hints

1. If `Xc = U S Vᵀ`, what is `Xcᵀ Xc` in terms of `V` and `S`? What does that make the eigenvalues of the covariance matrix?
2. The ratio divides one component's variance by the total. Does the `1 / (n − 1)` factor matter for the ratio?
3. What is the total variance of the data in terms of the columns alone, and how can you use it to check your sum?
4. Why would skipping the centering step give a first "component" that explains almost everything for data sitting far from the origin?

## Explain-back

- Someone keeps 3 components of a 50-column table "because 3 is easy to plot". What would you look at before choosing the number of components, and what cut-off might you use?
- Why does PCA on unscaled data (income in dollars, age in years) give a first component that is almost just income? When should you standardize first?
- The first two components explain 95% of the variance. Does that mean they hold 95% of the information needed to predict the label? Why not?
- You made a t-SNE plot and two clusters are far apart. Can you conclude they are very different? How is that different from distances along PCA components?
