# Gaussian anomaly detector

Topic: 16. Anomaly detection
Difficulty: 2 of 3

## Problem

Write a class `GaussianAnomalyDetector` with NumPy (allowed) that models each feature of normal rows as an independent Gaussian:

- `fit(X: np.ndarray) -> GaussianAnomalyDetector` takes a 2-D array of normal rows, stores each column's mean and variance (population variance, divide by `n`), and returns `self`. Raise `ValueError` if `X` is not 2-D, has no rows, or any column has variance 0.
- `score(X: np.ndarray) -> np.ndarray` returns, for each row, its log density: the sum over features `j` of `-0.5 * log(2π σⱼ²) - (xⱼ - μⱼ)² / (2 σⱼ²)`. Lower means more anomalous. Return a 1-D float array with one entry per row. Raise `RuntimeError` if called before `fit`.
- `choose_epsilon(scores: np.ndarray, labels: np.ndarray) -> tuple[float, float]` (a `@staticmethod`) picks the threshold on a labeled validation set. `labels` holds 1 for an anomaly and 0 for normal. A threshold `ε` flags every row with `score <= ε`. Try every distinct score value as `ε`, compute F1 of the flags against the labels (F1 is 0 when there is no true positive), and return `(ε, best_f1)` as floats for the best F1, taking the smallest `ε` on ties. Raise `ValueError` if the lengths differ or there is no anomaly in `labels`.

Fit on normal rows only; the labels are used only to choose `ε`.

## Examples

```
d = GaussianAnomalyDetector().fit(np.array([[0.0], [2.0]]))         mean 1, variance 1
d.score(np.array([[1.0], [3.0]]))                                     → [-0.9189, -2.9189]
GaussianAnomalyDetector.choose_epsilon(np.array([-10, -9, -3, -2, -1, 0]),
                                       np.array([1, 0, 1, 0, 0, 0])) → (-3.0, 0.8)
GaussianAnomalyDetector().fit(np.array([[1.0, 5.0], [2.0, 5.0]]))   → ValueError   column 2 has variance 0
```

## Constraints

- NumPy allowed; no scipy or scikit-learn in the solution.
- Up to 10 000 rows and 50 features; `score` is vectorized (no Python loop over rows).
- Scores within `1e-9` of the formula.

## Hints

1. For one feature, what is the log of the normal density at `x`? What does taking logs turn the product over features into, and why is that safer numerically?
2. Why must the mean and variance come from normal rows only? What happens to `σ²` if the anomalies are in the training data?
3. If you flag everything with `score <= ε`, which values of `ε` are worth trying, and why can no value in between do better?
4. With 2 anomalies in 1 000 rows, what accuracy does "flag nothing" get, and what F1?

## Explain-back

- Your training set accidentally includes the anomalies. What happens to the fitted means and variances, and to the scores of those anomalies?
- Why is `ε` chosen by F1 on a labeled validation set rather than by accuracy, and why not pick it with no labels at all?
- A feature is heavily right-skewed, like transaction amounts. Why does a Gaussian fit it badly, and what transform would you try first?
- You have 30 labeled fraud cases among a million transactions. Why is this still an anomaly-detection problem rather than a classification one?
