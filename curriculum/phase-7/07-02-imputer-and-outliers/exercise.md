# Imputer and outlier mask

Topic: 7. EDA, data cleaning and data quality
Difficulty: 2 of 3

## Problem

With pandas (required), write:

- A class `Imputer` with `fit(self, train: pd.DataFrame) -> "Imputer"` and `transform(self, df: pd.DataFrame) -> pd.DataFrame`. `fit` records the median of every numeric column of `train` (over its non-missing values) and returns `self`. `transform` returns a **new** DataFrame in which, for every fitted column, `NaN` is replaced by the stored train median and a boolean column `<col>_missing` is appended (in the order of the fitted columns, after the original columns) marking where a value was filled. Columns not seen in `fit` are copied unchanged. `transform` before `fit` raises `RuntimeError`. Neither method mutates its input, and the medians never change after `fit`, even if `transform` sees very different data.
- `iqr_outlier_mask(df: pd.DataFrame, k: float = 1.5) -> pd.DataFrame` — a boolean DataFrame with the same shape, index and columns as `df` (numeric columns only in `df`), `True` where a value is below `Q1 - k·IQR` or above `Q3 + k·IQR` of its column (quartiles by `Series.quantile`, which uses linear interpolation and skips `NaN`). `NaN` cells are `False`.

## Examples

```
train                 test
   a     b               a     b
0  1.0   10.0         0  NaN   NaN
1  NaN   20.0         1  9.0   1.0
2  3.0   NaN
3  5.0   40.0

imp = Imputer().fit(train)           medians: a 3.0, b 20.0
imp.transform(test)
     a     b  a_missing  b_missing
0  3.0  20.0       True       True
1  9.0   1.0      False      False

iqr_outlier_mask(pd.DataFrame({"x": [1, 2, 3, 4, 100]}))
       x
0  False
1  False
2  False
3  False
4   True
```

## Constraints

- Up to 100 000 rows and 50 columns; column operations only.
- Compared with `pandas.testing.assert_frame_equal` (dtype of the indicator columns must be bool).
- The train medians must be computed on `train` only; the test checks that `transform` on a shifted test set still uses them.

## Hints

1. Which DataFrame method selects only numeric columns, and which Series method gives a median that skips `NaN`?
2. `transform` must not change `df`. Which call gives you an independent copy to fill, and why is filling a view a bug?
3. The indicator must be computed before the fill. What would `df[col].isna()` return after `fillna`?
4. `Series.quantile(0.25)` and `quantile(0.75)` give the quartiles per column; broadcasting `df < lower` across columns gives a boolean frame. What does `NaN < 3` evaluate to?

## Explain-back

- Why are the medians stored at `fit` time and reused on test data, rather than recomputed on whatever `transform` receives? What breaks if the test set had its own medians?
- Why add a `<col>_missing` indicator at all? Give an example where missingness itself predicts the label.
- Median versus mean imputation on a column with a few huge values: which moves the filled values less, and why?
- `iqr_outlier_mask` flagged 4% of rows. List two reasons not to drop them and one situation where capping is better than dropping.
