# Pearson and Spearman correlation

Topic: 9. Inferential statistics and A/B testing
Difficulty: 2 of 3

## Problem

Write three functions in pure Python (no NumPy; `math` allowed):

- `pearson(x: list[float], y: list[float]) -> float` — `Σ(xᵢ - x̄)(yᵢ - ȳ) / sqrt(Σ(xᵢ - x̄)² Σ(yᵢ - ȳ)²)`. Raise `ValueError` if the lengths differ, there are fewer than 2 points, or either list is constant (the denominator is 0).
- `rank(values: list[float]) -> list[float]` — 1-based ranks with ties given the average of the positions they occupy: `rank([10, 20, 20, 30])` is `[1, 2.5, 2.5, 4]`.
- `spearman(x: list[float], y: list[float]) -> float` — the Pearson correlation of the two rank lists. Same errors as `pearson`.

## Examples

```
pearson([1, 2, 3], [2, 4, 6])              → 1.0
pearson([1, 2, 3], [3, 2, 1])              → -1.0
pearson([1, 2, 3, 4], [1, 3, 2, 4])        → 0.8
rank([10, 20, 20, 30])                     → [1.0, 2.5, 2.5, 4.0]
rank([5, 5, 5])                            → [2.0, 2.0, 2.0]
spearman([1, 2, 3, 4, 5], [1, 4, 9, 16, 25])   → 1.0     monotone, so rank correlation is perfect
pearson([1, 2, 3, 4, 5], [1, 4, 9, 16, 25])    → 0.98..
pearson([1, 1, 1], [1, 2, 3])              → ValueError  constant x
```

## Constraints

- Up to 10 000 points; `rank` must be O(n log n) (sort once), not O(n²).
- Must match `numpy.corrcoef` and `scipy`-style Spearman (average ranks) within `1e-9`; the test computes the expected values with NumPy.
- Results lie in `[-1, 1]` up to rounding.

## Hints

1. Pearson is a cosine similarity of two centred vectors. Which earlier function does that remind you of, and what do you subtract first?
2. To rank with ties, sort the indices by value, then walk the sorted order. When you meet a run of equal values, which positions do they occupy and what is their average?
3. Spearman is only one line once `rank` and `pearson` exist. What goes wrong if you rank the values without averaging ties?
4. When is the Pearson denominator zero, and why is the correlation undefined rather than 0 in that case?

## Explain-back

- Pearson is 0.98 and Spearman is 1.0 for `y = x²` on positive `x`. What does each coefficient measure, and when would you prefer Spearman?
- Correlation between ice-cream sales and drownings is 0.9. Name the confounder and say what experiment would separate cause from correlation.
- A Pearson correlation of 0 between `x` and `y`: does it mean they are unrelated? Give a shape of data with zero Pearson correlation and a clear relationship.
- Why does one huge outlier change Pearson a lot but Spearman only a little?
