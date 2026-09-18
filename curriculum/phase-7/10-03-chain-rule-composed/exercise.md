# Chain rule over a composition

Topic: 10. Derivatives and the chain rule
Difficulty: 2 of 3

## Problem

A chain of scalar functions is given as a list of `(f, f_prime)` pairs applied in order: `y = f_k(... f_2(f_1(x)))`. Write, in pure Python (no NumPy; `math` allowed):

- `compose(chain: list[tuple[Callable[[float], float], Callable[[float], float]]], x: float) -> float` — the value `y`.
- `chain_derivative(chain: list[tuple[Callable, Callable]], x: float) -> float` — `dy/dx` by the chain rule: walk the chain forward, keep the intermediate values, and multiply each local derivative **evaluated at its own input**. An empty chain is the identity: `compose` returns `x` and `chain_derivative` returns `1.0`.
- `intermediates(chain, x) -> list[float]` — the list `[x, f_1(x), f_2(f_1(x)), ..., y]` of length `len(chain) + 1`; the test uses it to check that you evaluate each derivative at the right point.

## Examples

```
sq = (lambda t: t * t, lambda t: 2 * t)
ex = (math.exp, math.exp)
sin = (math.sin, math.cos)

compose([sq, ex], 1.5)             → exp(2.25)
chain_derivative([sq, ex], 1.5)    → exp(2.25) * 3.0        d/dx exp(x²) = exp(x²) · 2x
chain_derivative([ex, sq], 1.5)    → 2 exp(1.5) · exp(1.5)  d/dx (exp x)² = 2 exp(x) · exp(x)
chain_derivative([sin, sq, ex], 0.7)   → numeric derivative of exp(sin(x)²) at 0.7
intermediates([sq, ex], 1.5)       → [1.5, 2.25, exp(2.25)]
chain_derivative([], 4.0)          → 1.0
```

## Constraints

- Chains of up to 20 functions.
- `chain_derivative` must match the central difference with `h = 1e-5` within `1e-6` on every test chain.
- Each function and each derivative is called exactly once per call to `chain_derivative`.

## Hints

1. For `y = g(f(x))`, `dy/dx = g'(f(x)) · f'(x)`. At which input is `g'` evaluated: `x` or `f(x)`?
2. Extend to three functions. Write out every factor and the point each is evaluated at. Do you see why you need the forward values before the derivatives?
3. What is the derivative of a composition of zero functions? What starting value for a running product gives that?
4. If you evaluated every `f_prime` at `x` instead of at its own input, which test chain would still pass by accident and which would fail?

## Explain-back

- The chain rule multiplies local derivatives; someone adds them instead. For `exp(x²)` at `x = 1.5`, what wrong number do they get, and how would a numeric check catch it?
- In backpropagation, the "local derivative" of each layer is multiplied into an incoming gradient. Which direction does that product get accumulated, and why does it start at 1?
- `chain_derivative([sigmoid_pair] * 10, 0.0)` is below `1e-6`, since every factor is at most `0.25`. What does that say about deep chains of saturating activations?
- Why does the numeric derivative of the whole composition need only two evaluations, while the analytic chain rule needs every intermediate value? Which is cheaper for one scalar, and which scales to millions of parameters?
