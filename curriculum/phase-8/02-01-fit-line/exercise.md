# Fit a line

Topic: 2. Linear regression and MSE, closed form
Difficulty: 1 of 3

## Problem

Write `fit_line(xs: list[float], ys: list[float]) -> tuple[float, float]` in pure Python (no numpy) that returns `(w, b)` for the line `ŷ = w·x + b` minimizing the mean squared error over the points.

Setting the derivatives of the MSE with respect to `w` and `b` to zero gives the answer in closed form:

- `w = Σ (xᵢ − x̄)(yᵢ − ȳ) / Σ (xᵢ − x̄)²`
- `b = ȳ − w·x̄`

The line must include the intercept `b`: data that does not pass through the origin has to be fitted as well as data that does.

Raise `ValueError` when:
- the lists have different lengths,
- there are fewer than 2 points,
- all `xs` are equal (no single best slope exists). Check the values themselves: with `xs = [0.1, 0.1, 0.1]` the float mean is not exactly `0.1`, so `Σ (xᵢ − x̄)²` comes out tiny but non-zero.

## Examples

```
fit_line([0, 1, 2], [1, 3, 5])        → (2.0, 1.0)
fit_line([1, 2, 3, 4], [2, 2, 2, 2])  → (0.0, 2.0)
fit_line([0, 1, 2, 3], [1, 0, 2, 1])  → (0.2, 0.7)
fit_line([3, 3, 3], [1, 2, 3])        → ValueError   vertical data
```

## Constraints

- Pure Python: `math` and `statistics` are allowed, numpy is not.
- Up to 100 000 points; O(n).
- Must match `numpy.polyfit(xs, ys, 1)` within `1e-8` (relative) on random data.

## Hints

1. Write the MSE as a function of `w` and `b` only. What are its two partial derivatives, and what do you get by setting the one for `b` to zero?
2. Once you know how `b` relates to the means, substitute it back. What is left to solve for `w`?
3. Why does the formula use deviations from the mean `(x − x̄)` instead of the raw `x`, and what does the denominator become when every `x` is the same?
4. What is the sum of the residuals `yᵢ − ŷᵢ` at the optimum, and what does that tell you about a line with no intercept?

## Explain-back

- Walk through the derivation: which equation does "the gradient equals zero" give for `b`, and which for `w`?
- If you drop `b` and fit `ŷ = w·x`, what happens on data like `y = 2x + 100`?
- The fitted line has R² = 0.98 for ice-cream sales against drownings. Does ice cream cause drowning? What does least squares actually tell you?
- One point has `y` a thousand times larger than the rest. How far does the line move, and why does squared error make it move that much?
