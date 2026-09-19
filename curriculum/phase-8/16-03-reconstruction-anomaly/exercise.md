# Reconstruction-error anomalies

Topic: 16. Anomaly detection
Difficulty: 3 of 3

## Problem

Some anomalies hide from every per-feature rule: each feature is in range, but the combination is not. Fit PCA on normal rows and score each row by how badly the top components reconstruct it. Write two functions with NumPy (allowed, including `np.linalg.svd` and `np.linalg.eigh`):

- `reconstruction_errors(X_train: np.ndarray, X: np.ndarray, n_components: int) -> np.ndarray`:
  1. Compute the column means `μ` of `X_train` (not of `X`).
  2. Find the top `n_components` principal directions of `X_train - μ`: the right singular vectors with the largest singular values (equivalently, the eigenvectors of the covariance matrix with the largest eigenvalues). Stack them as the rows of `W`, shape `(n_components, d)`.
  3. For each row `x` of `X`: project `z = W (x - μ)`, reconstruct `x̂ = μ + Wᵀ z`, and score it by the squared error `‖x - x̂‖²` (a sum over features, not a mean).

  Return a 1-D float array with one score per row of `X`. No feature scaling. Raise `ValueError` if `n_components` is not in `1..d`, if either array is not 2-D, or if the two arrays have different numbers of columns.
- `top_anomalies(errors: np.ndarray, n: int) -> list[int]` returns the indices of the `n` largest errors, largest first, lower index first on ties. If `n` exceeds the number of rows, return all of them.

## Examples

```
X_train = np.array([[0.0, 0.0], [1.0, 1.0], [2.0, 2.0], [3.0, 3.0]])   every row on the line y = x
reconstruction_errors(X_train, np.array([[5.0, 5.0], [1.0, 2.0]]), 1) → [0.0, 0.5]   (1, 2) reconstructs to (1.5, 1.5)
reconstruction_errors(X_train, np.array([[1.0, 2.0]]), 2)             → [0.0]        all components: nothing is lost
reconstruction_errors(X_train, np.array([[1.0, 2.0]]), 3)             → ValueError
top_anomalies(np.array([0.1, 0.5, 0.2, 0.5]), 3)                      → [1, 3, 2]
```

## Constraints

- NumPy allowed; no scikit-learn in the solution.
- Up to 5 000 rows and 50 features; no Python loop over rows.
- Errors within `1e-6` of the test's own PCA computation.

## Hints

1. If every normal row lies close to a line through the data, what does projecting a normal row onto that line lose, and what does it lose for a row that is off the line?
2. After `np.linalg.svd(Xc, full_matrices=False)`, which of the returned matrices holds the directions, and are they in rows or columns?
3. Why must the centering mean come from `X_train`, even when you score a single new row?
4. What is the reconstruction error of every row when you keep all `d` components, and what does that say about how to choose `n_components`?

## Explain-back

- In the test data every feature of the planted anomalies is within the normal range. Why do z-score and IQR rules miss them while reconstruction error catches them?
- What goes wrong if the PCA is fitted on data that already contains many anomalies?
- One feature is in dollars and another in millions of dollars. How does the missing scaling change which directions PCA keeps, and what would you do about it?
- You still need a threshold on these scores. How would you pick it, and what would you report besides the threshold?
