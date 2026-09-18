# Data quality report

Topic: 7. EDA, data cleaning and data quality
Difficulty: 3 of 3

## Problem

Write `quality_report(train: pd.DataFrame, test: pd.DataFrame, k: float = 3.0) -> dict[str, object]` with pandas (required). `train` and `test` have the same columns. Return a dict with:

- `"duplicate_rows"` — `int`, the number of rows in `train` that are exact duplicates of an earlier row (`DataFrame.duplicated().sum()`).
- `"missing_rate"` — a float `Series` indexed by column (in `train`'s column order) with the fraction of `NaN` per column of `train`.
- `"constant_columns"` — `list[str]` of columns whose non-missing values in `train` take a single distinct value (a column that is entirely `NaN` counts as constant).
- `"id_like_columns"` — `list[str]` of columns whose non-missing values in `train` are all distinct and there are at least 2 of them (every row its own value: an identifier, not a feature).
- `"drifted_columns"` — `list[str]` of numeric columns where `|mean_test - mean_train| > k * std_train` (means and `std` with `ddof=1` over non-missing values). Columns with `std_train == 0` or `NaN` are never reported as drifted.

Lists keep `train`'s column order. Do not modify the inputs.

## Examples

```
train                                   test
   id  const  x      y  label            id  const  x      y  label
0   1     7   1.0  NaN     0          0  10     7  50.0  1.0     1
1   2     7   2.0  2.0     1          1  11     7  51.0  2.0     0
2   3     7   3.0  3.0     0
3   3     7   3.0  3.0     0            (row 3 duplicates row 2)

quality_report(train, test, k=3)
duplicate_rows     → 1
missing_rate       → id 0.0, const 0.0, x 0.0, y 0.25, label 0.0
constant_columns   → ["const"]
id_like_columns    → []          the duplicate row makes id 3 appear twice
drifted_columns    → ["id", "x"] x: train mean 2.25, std ~0.96, test mean 50.5
```

## Constraints

- Up to 200 000 rows and 100 columns; column operations only.
- `missing_rate` is compared with `pandas.testing.assert_series_equal` at `1e-9`; the lists and count with equality.
- Non-numeric columns are skipped by the drift check but included in the other checks.

## Hints

1. `df.duplicated()` marks which rows? The first occurrence or the later ones? Check with the example.
2. `Series.nunique()` skips `NaN` by default and `Series.count()` counts non-missing values. How do those two numbers identify a constant column and an ID-like column?
3. Which method keeps only numeric columns so `mean()` and `std()` do not choke on text?
4. For the drift check, the comparison `(test.mean() - train.mean()).abs() > k * train.std()` works column by column. What happens when `std` is `0` or `NaN`, and how do you keep those columns out?

## Explain-back

- Why is a column where every row has its own value useless as a feature, and how could a tree model still "use" it to reach 100% training accuracy?
- A `train` column is correlated 0.99 with the label. Before celebrating, what would you check about how that column was collected?
- A `k = 3` drift flag fired for `x`. What could cause a test-set mean far from the train mean, and why does that make the reported test accuracy untrustworthy?
- Why should this report be regenerated every time new data arrives, rather than run once? Give one failure it would catch late.
