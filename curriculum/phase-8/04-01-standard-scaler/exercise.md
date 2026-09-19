# Standard scaler

Topic: 4. Features: scaling, encoding and feature engineering
Difficulty: 1 of 3

## Problem

Write a `StandardScaler` class with NumPy that learns per-column statistics from the training rows and applies exactly those statistics to any rows later.

- `fit(self, train: np.ndarray) -> "StandardScaler"` — `train` has shape `(n, d)` with `n ≥ 1`. Store `self.mean_ = train.mean(axis=0)` and `self.scale_`, the population standard deviation per column (`train.std(axis=0)`), except that a column whose standard deviation is `0` gets `scale_ = 1.0` so it transforms to all zeros instead of dividing by zero. Return `self`. Raise `ValueError` if `train` is not 2-D or has no rows.
- `transform(self, rows: np.ndarray) -> np.ndarray` — return a new array `(rows − mean_) / scale_` using only the stored statistics; it never looks at `rows` to compute anything. Works for any number of rows, including one. Raise `RuntimeError` if called before `fit`, and `ValueError` if `rows` is not 2-D or its column count differs from the fitted one. Never modify `rows` in place.

After `fit(train)`, `transform(train)` has column means `0` and standard deviations `1` (except constant columns, which are `0`), and the result matches `sklearn.preprocessing.StandardScaler` within `1e-12`. Validation and test rows transformed with the same scaler are generally *not* mean 0, and that is correct.

## Examples

```
s = StandardScaler().fit(np.array([[1.0, 5.0], [3.0, 5.0]]))
s.mean_                                  → [2.0, 5.0]
s.scale_                                 → [1.0, 1.0]        column 2 is constant
s.transform(np.array([[1.0, 5.0]]))      → [[-1.0, 0.0]]
s.transform(np.array([[7.0, 9.0]]))      → [[5.0, 4.0]]      train statistics, not these rows'
StandardScaler().transform(np.ones((1, 2)))  → RuntimeError
```

## Constraints

- NumPy allowed; scikit-learn is not.
- Up to 100 000 rows and 100 columns; vectorized, no Python loop over rows.
- Accept integer arrays too: the output is always float.

## Hints

1. Which rows are you allowed to learn the mean and standard deviation from, and what would it mean if the test rows helped compute them?
2. If `transform` computed `rows.mean(axis=0)` itself, what would it return for a single row, whatever the row is?
3. A column holds the same value in every training row. What is its standard deviation, what does division do with that, and what value is a sensible output for that column?
4. How can you tell, inside `transform`, whether `fit` has been called?

## Explain-back

- You fit the scaler on the full dataset and then split into train and test. What leaked, and in which direction does it bias the test score?
- Which of these need scaled features and which do not: linear regression trained by gradient descent, kNN, PCA, a decision tree? Why the difference?
- After scaling with train statistics, the test set's column means are 0.3, not 0. Is something broken?
- A feature is constant in training but varies in production. What does your scaler output for it, and should that worry you?
