# Numeric gradient

Topic: 11. Partial derivatives, gradients and Jacobians
Difficulty: 1 of 3

## Problem

Write `numeric_gradient(f: Callable[[list[float]], float], params: list[float], h: float = 1e-5) -> list[float]` in pure Python (no NumPy).

`f` takes a list of parameters and returns a scalar. The gradient is the list of partial derivatives, one per parameter, each by a central difference: nudge parameter `i` up by `h` and down by `h` while holding every other parameter fixed, and divide the difference of `f` by `2h`. The result has the same length as `params`. Do not modify `params`. Raise `ValueError` if `h <= 0`.

## Examples

```
numeric_gradient(lambda p: p[0]**2 + p[1]**2, [1.0, 2.0])      → [2.0, 4.0]
numeric_gradient(lambda p: p[0] * p[1], [3.0, 5.0])            → [5.0, 3.0]     interacting parameters
numeric_gradient(lambda p: 3 * p[0] - p[1] + 7, [10.0, -1.0])  → [3.0, -1.0]
numeric_gradient(lambda p: sum(x**2 for x in p), [0.0, 0.0, 0.0])  → [0.0, 0.0, 0.0]   a minimum
numeric_gradient(lambda p: 5.0, [1.0, 2.0])                    → [0.0, 0.0]
```

## Constraints

- Up to 1 000 parameters; the function is called exactly `2 · len(params)` times.
- Results within `1e-6` of the analytic gradient on smooth functions with values of order 1.
- `params` is unchanged after the call, and `f` never sees a list with more than one parameter nudged at once.

## Hints

1. A partial derivative holds every other coordinate fixed. Which coordinate changes between the two calls to `f` for entry `i`, and by how much?
2. If you nudge `params[i] += h` in place and forget to restore it, what does the next partial derivative measure?
3. `f(p) = p[0] · p[1]`: the partial with respect to `p[0]` depends on `p[1]`. Does your loop evaluate at the right `p[1]`?
4. How many calls to `f` does the whole gradient take for `n` parameters, and what does that cost for a model with a million weights?

## Explain-back

- The gradient of `f(p) = p[0]² + p[1]²` at `[1, 2]` is `[2, 4]`. What does the direction `[2, 4]` mean for the value of `f`? Which direction decreases it fastest?
- Why does the gradient live in parameter space and have the same shape as `params`, not the shape of the inputs to the model?
- A gradient check on a loss of size `1e6` reports an absolute error of `1e-2`. Is the analytic gradient wrong? What measure would you use instead?
- Numeric gradients are exact up to `O(h²)` and float noise. Why are they still never used for training, only for checking?
