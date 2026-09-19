# Polynomial regression

Topic: 2. Linear regression and MSE, closed form
Difficulty: 2 of 3

## Problem

A cubic curve is still *linear* regression: the model `ŷ = c₀ + c₁x + c₂x² + c₃x³` is linear in the parameters `c`, so the normal equations solve it. Write three pure-Python functions (no numpy):

- `solve(a: list[list[float]], b: list[float]) -> list[float]` — your Phase 7 Gaussian-elimination solver with partial pivoting (copy it in). Raise `ValueError` for a shape mismatch or when a pivot's absolute value is below `1e-12` (singular).
- `polynomial_features(xs: list[float], degree: int) -> list[list[float]]` — one row per `x`: `[1, x, x², …, x^degree]` (the leading `1` is the bias column). Raise `ValueError` if `degree < 0`.
- `fit_polynomial(xs: list[float], ys: list[float], degree: int) -> list[float]` — build `X = polynomial_features(xs, degree)`, form `XᵀX` and `Xᵀy`, and return the coefficients `[c₀, c₁, …, c_degree]` from `solve(XᵀX, Xᵀy)`. Never form an explicit inverse. Raise `ValueError` if the lengths differ, and let `solve` raise `ValueError` when `XᵀX` is singular, which happens when there are fewer distinct `x` values than coefficients.

## Examples

```
polynomial_features([2, 3], 2)                      → [[1, 2, 4], [1, 3, 9]]
polynomial_features([5], 0)                         → [[1]]
fit_polynomial([0, 1, 2], [1, 3, 5], 1)             → [1.0, 2.0]
fit_polynomial([-2, -1, 0, 1, 2, 3], ys, 3)         → [2.0, -1.0, 0.5, 3.0]   for ys = 2 - x + 0.5x² + 3x³
fit_polynomial([1, 2, 3, 4], [5, 1, 4, 2], 0)       → [3.0]                    the mean
fit_polynomial([0, 0, 1, 1, 2, 2], ys, 3)           → ValueError               3 distinct xs, 4 coefficients
```

## Constraints

- Pure Python: `math` is allowed, numpy is not.
- `xs` within `[-3, 3]`, degree at most 5, at most 200 points.
- Coefficients of an exact cubic recovered within `1e-8`; noisy fits match `numpy.polyfit` within `1e-6`.

## Hints

1. Write the prediction for one row as a dot product. Which vector holds the data and which holds the parameters, and in which of the two is the model linear?
2. How do you compute `(XᵀX)[i][j]` and `(Xᵀy)[i]` as sums over the rows, without building `Xᵀ` explicitly?
3. With four data points at only three distinct `x` values, how many independent rows does `X` have, and what does that do to `XᵀX`?
4. `numpy.polyfit` returns the highest power first. What order does your function return, and how must you compare the two?

## Explain-back

- Why is fitting `ŷ = c₀ + c₁x + c₂x² + c₃x³` called linear regression, when the curve is not a line?
- You fit a degree-9 polynomial to 10 points and the training MSE is 0. Is that a good model? What would the validation MSE show?
- Why solve `(XᵀX)c = Xᵀy` with elimination instead of computing `(XᵀX)⁻¹ Xᵀy`?
- Where did the bias term go in this model, and what would happen to the fit if you dropped the column of ones?
