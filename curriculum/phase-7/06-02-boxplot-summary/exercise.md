# Box plot summary

Topic: 6. Visualization with matplotlib
Difficulty: 2 of 3

## Problem

Write `boxplot_summary(values: list[float]) -> dict[str, object]` in pure Python (no NumPy) that computes exactly the numbers a matplotlib box plot draws:

- `"q1"`, `"median"`, `"q3"` — the 25th, 50th and 75th percentiles with linear interpolation between sorted neighbours (NumPy's default: position `p * (n - 1)` in the sorted list).
- `"iqr"` — `q3 - q1`.
- `"whisker_low"` — the smallest value that is `>= q1 - 1.5 * iqr`; `"whisker_high"` — the largest value that is `<= q3 + 1.5 * iqr`. Whiskers end on data points, not on the fence itself.
- `"outliers"` — every value outside the two whiskers, in the original order.

Raise `ValueError` on an empty list. Do not modify the input.

## Examples

```
boxplot_summary([1, 2, 3, 4, 5, 6, 7, 8, 9, 30])
→ q1 3.25, median 5.5, q3 7.75, iqr 4.5,
  whisker_low 1, whisker_high 9, outliers [30]

boxplot_summary([5])
→ q1 5, median 5, q3 5, iqr 0, whisker_low 5, whisker_high 5, outliers []

boxplot_summary([4, 1, 3, 2])
→ q1 1.75, median 2.5, q3 3.25
```

## Constraints

- Up to 100 000 values; sort once.
- Must match `matplotlib.cbook.boxplot_stats` (keys `q1`, `med`, `q3`, `iqr`, `whislo`, `whishi`, `fliers`) within `1e-9`.
- Whiskers are data values, so `whisker_low >= min(values)`.

## Hints

1. For a sorted list of length `n`, the 25th percentile sits at position `0.25 * (n - 1)`. What do you do when that position is `2.25`?
2. The fences are `q1 - 1.5 iqr` and `q3 + 1.5 iqr`. Is the whisker drawn at the fence or at a data point? Check the first example: the fence is `-3.5` but the whisker is `1`.
3. Which values are outliers once you know the two whiskers? Can a value equal to a whisker be an outlier?
4. With one value, what are the quartiles, the IQR and the whiskers? Does your percentile code survive `n - 1 == 0`?

## Explain-back

- The box in a box plot spans which values? Why is reading it as "the range of the data" wrong, and what fraction of the data does it hold?
- Why 1.5 × IQR? What does the choice imply about how many points a normal sample flags as outliers?
- Two groups have the same median but one box is three times taller. What does that tell you that a bar chart of the means would hide?
- A value flagged as an outlier by the box plot: should it be removed? Name one reason to keep it and one to investigate it.
