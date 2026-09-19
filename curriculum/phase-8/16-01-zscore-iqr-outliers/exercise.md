# Z-score and IQR outliers

Topic: 16. Anomaly detection
Difficulty: 1 of 3

## Problem

The two oldest anomaly rules look at one feature at a time. Write two pure-Python functions that return one boolean flag per value, in input order (`True` means "flag as an outlier"):

- `zscore_flags(xs: list[float], k: float = 3.0) -> list[bool]` flags `x` when `|x - mean| / std > k` (strictly greater). Use the population standard deviation (divide by `n`, not `n - 1`). If the standard deviation is 0, nothing is flagged.
- `iqr_flags(xs: list[float], factor: float = 1.5) -> list[bool]` flags `x` when `x < Q1 - factor * IQR` or `x > Q3 + factor * IQR` (strict), where `IQR = Q3 - Q1`. Compute the quartiles by linear interpolation: sort the values, and the `p`-quantile sits at position `p * (n - 1)` in the sorted list (0-based), interpolating between the two neighbours when that position is fractional. This is NumPy's default `np.percentile` and `statistics.quantiles(xs, n=4, method="inclusive")`. A single value has `Q1 = Q3` and is not flagged.

Both raise `ValueError` on an empty list.

## Examples

```
zscore_flags([1, 2, 3, 4, 5, 100], k=2.0)  → [False, False, False, False, False, True]    z of 100 ≈ 2.23
zscore_flags([1, 2, 3, 4, 5, 100], k=3.0)  → [False, False, False, False, False, False]   100 inflated the std it is judged by
iqr_flags([1, 2, 3, 4, 5, 100])            → [False, False, False, False, False, True]    Q1 = 2.25, Q3 = 4.75, fences -1.5 and 8.5
zscore_flags([7, 7, 7])                    → [False, False, False]
iqr_flags([])                              → ValueError
```

## Constraints

- Pure Python: `math` and `statistics` are allowed, numpy is not.
- At most 100 000 values; O(n log n) is fine.

## Hints

1. What is the mean and the standard deviation of `[1, 2, 3, 4, 5, 100]`, and how much of that standard deviation comes from the 100 alone?
2. Which of the two rules is built from statistics that one extreme value can drag, and which from statistics that barely move?
3. For 6 sorted values, at what position does the 0.25-quantile sit, and which two values do you interpolate between?
4. What should happen when every value is identical, and why would dividing by the standard deviation be a problem there?

## Explain-back

- Why did the z-score rule miss 100 at `k = 3` while the IQR rule caught it? What is this "masking" effect?
- A feature is heavily right-skewed (incomes, transaction amounts). What happens to both rules, and what would you transform first?
- Each rule looks at one feature. Describe a row that is anomalous even though every one of its features is inside the normal range.
- Someone tunes `k` until the flags "look right" without any labeled example. What is missing from that process?
