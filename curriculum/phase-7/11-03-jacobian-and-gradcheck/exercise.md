# Jacobian and gradient check

Topic: 11. Partial derivatives, gradients and Jacobians
Difficulty: 3 of 3

## Problem

Write two functions in pure Python (no NumPy; `math` allowed):

- `numeric_jacobian(f: Callable[[list[float]], list[float]], x: list[float], h: float = 1e-5) -> list[list[float]]` — for `f: Rⁿ → Rᵐ`, the `m×n` matrix `J[i][j] = ∂fᵢ/∂xⱼ` by central differences, one column per input nudged. Determine `m` from `f(x)`. Raise `ValueError` if `h <= 0` or `x` is empty.
- `gradient_check(analytic: list[float], numeric: list[float]) -> float` — the relative error `‖a - n‖₂ / max(‖a‖₂ + ‖n‖₂, 1e-12)` between two gradients of equal length. Raise `ValueError` on a length mismatch. Two zero gradients give `0.0`. A relative error below about `1e-6` means the analytic gradient is trustworthy; above `1e-3` it is wrong.

## Examples

```
f = lambda v: [v[0] * v[1], v[0] + v[1], v[0] ** 2]     R² → R³
numeric_jacobian(f, [2.0, 3.0])
→ [[3.0, 2.0],
   [1.0, 1.0],
   [4.0, 0.0]]

numeric_jacobian(lambda v: [v[0]], [1.5])   → [[1.0]]

gradient_check([2.0, 4.0], [2.0000001, 4.0])   → about 1.6e-8      passes
gradient_check([2.0, 4.0], [2.0, 4.0])         → 0.0
gradient_check([2.0, 4.0], [2.0, 4.4])         → about 0.03        fails
gradient_check([1e6, 1e6], [1e6 + 1, 1e6])     → about 3.5e-7      tiny relative error despite absolute error 1
gradient_check([0.0, 0.0], [0.0, 0.0])         → 0.0
```

## Constraints

- Up to 50 inputs and 50 outputs; `2n` calls to `f`.
- Jacobian entries within `1e-6` of the analytic ones on the test functions.
- `gradient_check` must be scale-free: multiplying both gradients by `1e6` leaves the error unchanged.

## Hints

1. Nudging input `j` changes every output at once. Which column of the Jacobian does one pair of `f` calls fill, and how do you place `m` values into it?
2. What are the dimensions of `J` for `f: Rⁿ → Rᵐ`, and which index is the output? Check with the `R² → R³` example: 3 rows or 3 columns?
3. Why divide the error by the size of the gradients rather than report `‖a - n‖` alone? Try both on the `1e6` example.
4. What happens to the ratio when both gradients are exactly zero, and why is the `1e-12` in the denominator there?

## Explain-back

- For a scalar loss, the Jacobian has one row and it is the gradient. What shape does the Jacobian of a layer `R⁷⁸⁴ → R²⁵⁶` have, and why does backprop never build it explicitly?
- The chain rule for vector functions multiplies Jacobians. In `R² → R³ → R¹`, what are the shapes being multiplied and what is the result's shape?
- A gradient check reports `1e-2`. List two possible causes in the analytic code and one cause that is not a bug (hint: kinks).
- Why must a gradient check compare relative error, and what would an absolute threshold of `1e-6` do to a check on a loss with gradients of size `1e6`?
