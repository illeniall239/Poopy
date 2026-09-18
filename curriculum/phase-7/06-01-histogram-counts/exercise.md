# Histogram counts

Topic: 6. Visualization with matplotlib
Difficulty: 1 of 3

## Problem

Write `histogram(values: list[float], bins: int) -> tuple[list[int], list[float]]` in pure Python (no NumPy) that returns `(counts, edges)` exactly as `np.histogram(values, bins)` does:

- `edges` has `bins + 1` equally spaced values from `min(values)` to `max(values)` inclusive.
- Bin `i` covers `[edges[i], edges[i+1])` — closed on the left, open on the right — except the last bin, which is closed on both ends so the maximum value is counted.
- `counts[i]` is the number of values falling in bin `i`; the counts sum to `len(values)`.
- If every value is the same, use the range `[v - 0.5, v + 0.5]` (what NumPy does).

Raise `ValueError` if `values` is empty or `bins < 1`.

## Examples

```
histogram([1, 2, 2, 3, 4], 3)   → ([1, 2, 2], [1.0, 2.0, 3.0, 4.0])
                                    bins [1,2), [2,3), [3,4]: the 4 lands in the last bin
histogram([0, 10], 2)           → ([1, 1], [0.0, 5.0, 10.0])
histogram([5, 5, 5], 2)         → ([0, 3], [4.5, 5.0, 5.5])
histogram([], 3)                → ValueError
```

## Constraints

- Up to 100 000 values and 1 000 bins; work out the bin index arithmetically rather than scanning every edge per value.
- Counts must match `np.histogram` exactly and edges within `1e-9`.
- Values with float noise near an edge should land where NumPy puts them; use the same formula `edges[i] = lo + i * (hi - lo) / bins`.

## Hints

1. Given `lo`, `hi` and `bins`, what single arithmetic expression maps a value to the index of its bin? What does it give for `hi` itself?
2. How do you make the maximum value fall into the last bin rather than into a non-existent bin `bins`?
3. `edges` could be built by repeatedly adding the width. Why is `lo + i * width` safer than accumulating?
4. Why does NumPy widen the range by 0.5 on each side when all values are equal, and what would a zero-width bin do to your index formula?

## Explain-back

- The same data in 3 bins looks unimodal and in 30 bins looks bimodal. Which is "right", and what would you do before making a claim?
- Why is the last bin closed on both ends? What would happen to the maximum without that rule?
- A histogram and a bar chart both draw rectangles. What is different about the x axis, and when would a bar chart be wrong?
- Someone drew a histogram with 3 bins and said "no outliers". What can and cannot a 3-bin histogram show?
