# Numeric derivative

Topic: 10. Derivatives and the chain rule
Difficulty: 1 of 3

## Problem

Write two functions in pure Python (no NumPy; `math` allowed):

- `numeric_derivative(f: Callable[[float], float], x: float, h: float = 1e-5) -> float` — the central difference `(f(x + h) - f(x - h)) / (2h)`. Raise `ValueError` if `h <= 0`.
- `forward_derivative(f: Callable[[float], float], x: float, h: float = 1e-5) -> float` — the forward difference `(f(x + h) - f(x)) / h`, kept so you can compare the two. Same check on `h`.

`f` is any function from float to float.

## Examples

```
numeric_derivative(lambda x: x**2, 3.0)            → 6.0 (within 1e-8)
numeric_derivative(math.sin, 0.0)                  → 1.0
numeric_derivative(math.exp, 1.0)                  → 2.71828...
numeric_derivative(lambda x: x**3, 2.0, h=1e-2)    → 12.0001   error ~ h²
forward_derivative(lambda x: x**3, 2.0, h=1e-2)    → 12.0601   error ~ h
numeric_derivative(math.exp, 0.0, h=0.0)           → ValueError
```

## Constraints

- With `h = 1e-5` the central difference must be within `1e-8` of the true derivative for smooth functions with values of order 1.
- For `f(x) = x³` at `x = 2`, the central-difference error must shrink by about 100× when `h` goes from `1e-2` to `1e-3` (second-order), and the forward error by about 10× (first-order).
- Exactly two evaluations of `f` per call for the central version.

## Hints

1. Draw a curve and mark `x - h`, `x`, `x + h`. Which two points does the central difference connect, and why is that chord's slope closer to the tangent than the forward one?
2. Expand `f(x + h)` and `f(x - h)` as Taylor series to the `h³` term. Which terms cancel when you subtract?
3. `h = 1e-12` sounds "more precise". `f(x + h) - f(x - h)` then differs in which decimal place of a float, and how many digits does that leave?
4. If the test counts calls to `f`, what is the minimum number for the central difference?

## Explain-back

- Why does the central-difference error scale as `h²` while the forward-difference error scales as `h`? Which one would you choose for gradient checking?
- Shrinking `h` from `1e-5` to `1e-10` makes the numeric derivative worse. Which two error sources compete, and roughly where is the sweet spot for float64?
- A network has 10 million parameters. How many forward passes would a numeric gradient need, and why is that unusable for training even though it is fine for checking?
- What is the derivative as a "best local linear approximation"? Write the approximation for `f(x + Δ)` and say what the numeric derivative estimates.
