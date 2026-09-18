# Activation functions and their derivatives

Topic: 10. Derivatives and the chain rule
Difficulty: 2 of 3

## Problem

Write six scalar functions in pure Python (no NumPy; `math` allowed):

- `sigmoid(x: float) -> float` — `1 / (1 + e^(-x))`, numerically safe for `x = -1000` and `x = 1000` (no `OverflowError`).
- `sigmoid_prime(x: float) -> float` — `σ(x) (1 - σ(x))`.
- `tanh(x: float) -> float` — the hyperbolic tangent (`math.tanh` is fine).
- `tanh_prime(x: float) -> float` — `1 - tanh(x)²`.
- `relu(x: float) -> float` — `max(0, x)`.
- `relu_prime(x: float) -> float` — `1.0` for `x > 0`, `0.0` for `x <= 0` (the subgradient convention at the kink).

## Examples

```
sigmoid(0.0)          → 0.5
sigmoid(1000.0)       → 1.0
sigmoid(-1000.0)      → 0.0
sigmoid_prime(0.0)    → 0.25
tanh_prime(0.0)       → 1.0
relu(-2.0)            → 0.0
relu_prime(0.0)       → 0.0
relu_prime(3.0)       → 1.0
```

## Constraints

- Each derivative must match the central difference `(f(x+h) - f(x-h)) / 2h` with `h = 1e-5` within `1e-7` at 200 points in `[-6, 6]` (`relu_prime` is checked away from 0).
- `sigmoid_prime` must be at most `0.25` everywhere and `tanh_prime` at most `1.0`.
- `sigmoid(-1000)` must return exactly `0.0` or a tiny positive number, never raise.

## Hints

1. `math.exp(1000)` overflows. For which sign of `x` does `1 / (1 + exp(-x))` compute `exp` of a large positive number, and what equivalent formula avoids it?
2. Differentiate `σ(x) = (1 + e^(-x))^(-1)` with the chain rule, then rewrite the result using `σ(x)` itself. Why is that rewrite convenient inside a neural network?
3. `d/dx tanh(x) = 1 - tanh²(x)`. Where is it largest, and what happens to it for `|x| > 4`? What does that mean for gradients flowing through many tanh layers?
4. `relu` has a corner at 0. What are the left and right derivatives, and why does picking either value work in practice?

## Explain-back

- `sigmoid_prime` never exceeds `0.25`. Multiply ten of them together along a chain: what size is the product, and which training problem does that name?
- Is ReLU differentiable at 0? Why does that not stop gradient descent, and what is the probability a float activation lands exactly on 0?
- Why express `σ'` as `σ(1 - σ)` rather than recomputing `e^(-x)`? Which value is already available during backpropagation?
- A colleague implements `sigmoid` as `1 / (1 + math.exp(-x))` and it works on all their tests. Give an input that crashes it and one that silently returns a wrong `0.0`.
