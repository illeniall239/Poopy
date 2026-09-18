# Describe a column

Topic: 7. EDA, data cleaning and data quality
Difficulty: 1 of 3

## Problem

Write `describe_column(s: pd.Series) -> pd.Series` with pandas (required). The input is a numeric Series that may contain `NaN`. Return a Series indexed, in this order, by:

`count`, `missing`, `mean`, `median`, `std`, `skewness`, `min`, `max`

where `count` is the number of non-missing values, `missing` the number of `NaN`s, and every statistic is computed over the non-missing values only. `std` uses `ddof=1` (pandas' default). `skewness` is the sample skewness pandas' `Series.skew()` computes (adjusted Fisher–Pearson). When fewer than 3 values are present `skewness` is `NaN`; when fewer than 2, `std` is `NaN` too.

Raise `ValueError` if every value is missing. Do not modify `s`.

## Examples

```
describe_column(pd.Series([1.0, 2.0, np.nan, 4.0, 100.0]))
count       4.0
missing     1.0
mean       26.75
median      3.0
std        48.8..
skewness    1.99..
min         1.0
max       100.0

describe_column(pd.Series([3.0, np.nan]))  → count 1, missing 1, mean 3, std NaN, skewness NaN
describe_column(pd.Series([np.nan, np.nan]))  → ValueError
```

## Constraints

- Up to 1 000 000 values; use Series methods, no Python loops.
- Compared with NumPy on the non-missing values within `1e-9` using `pandas.testing.assert_series_equal`.
- The result's dtype is float.

## Hints

1. Which Series method tells you, per element, whether it is missing? How do you turn that into a count?
2. Do `s.mean()`, `s.std()` and `s.median()` skip `NaN` by default? What about `np.mean` on the same values?
3. `std` with `ddof=1` divides by `n - 1`. What does that give for a single value, and does pandas raise or return `NaN`?
4. How do you build a Series from a dict so the index comes out in the order you listed the keys?

## Explain-back

- The mean is 26.75 and the median 3.0. Which describes "a typical value" better here, and which statistic told you the distribution is skewed?
- `s.mean()` skipped the `NaN`; `np.mean(s.to_numpy())` returned `NaN`. When is silently skipping dangerous?
- Why does `std` divide by `n - 1` for a sample, and when would `ddof=0` be the right choice?
- Someone imputes a column's missing values with its own mean before a train/test split. What information leaks, and why does the standard deviation shrink?
