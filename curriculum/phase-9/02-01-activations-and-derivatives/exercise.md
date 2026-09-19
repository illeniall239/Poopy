# Activations and their derivatives

Topic: 2. Activation functions
Difficulty: 1 of 3

## Problem

Write ten functions in plain Python (the `math` module is fine; no numpy, no torch). Each takes one float `x` and returns a float.

- `sigmoid(x)` = `1 / (1 + e^(−x))` and `d_sigmoid(x)`, its derivative. Neither may raise `OverflowError` for `|x|` up to `1000`: `sigmoid(-1000)` is `0.0` (or a tiny positive number) and `sigmoid(1000)` is `1.0`.
- `tanh(x)` and `d_tanh(x)`. You may call `math.tanh` inside `tanh`.
- `relu(x)` = `max(0, x)` and `d_relu(x)`. At exactly `x = 0` use the convention PyTorch uses: `d_relu(0) = 0`.
- `leaky_relu(x, alpha=0.01)` = `x` if `x > 0` else `alpha · x`, and `d_leaky_relu(x, alpha=0.01)`. At exactly `x = 0` the derivative is `alpha`.
- `gelu(x)` = `x · Φ(x)`, the exact GELU, where `Φ(x) = ½(1 + erf(x / √2))` is the standard normal CDF, and `d_gelu(x)`, its derivative. Use `math.erf`.

Every derivative is checked against a central-difference numeric derivative `(f(x + h) − f(x − h)) / 2h` with `h = 1e-6`, within `1e-6`, at points away from the ReLU kink.

## Examples

```
sigmoid(0.0)        → 0.5
d_sigmoid(0.0)      → 0.25
d_tanh(0.0)         → 1.0
relu(-2.0)          → 0.0
d_relu(0.0)         → 0.0
leaky_relu(-2.0)    → -0.02
d_leaky_relu(-2.0)  → 0.01
gelu(1.0)           → 0.8413447460685429
d_gelu(0.0)         → 0.5
d_sigmoid(20.0)     → 2.06e-09              saturated: almost no gradient
```

## Constraints

- Inputs are finite floats with `|x| ≤ 1000`.
- Plain Python and `math` only.

## Hints

1. Can you write `d_sigmoid` and `d_tanh` using only the function's own output? Why is that handy in a backward pass?
2. `e^(−x)` overflows when `x` is very negative. Which equivalent form of the sigmoid avoids a huge exponent when `x < 0`?
3. ReLU has a corner at 0, so it has no true derivative there. Does the value you pick at that single point matter in practice?
4. `gelu(x)` is a product `x · Φ(x)`. What does the product rule give, and what is the derivative of the normal CDF `Φ`?

## Explain-back

- `d_sigmoid(20)` is about `2e-9` and `d_sigmoid` is never more than `0.25`. What happens to the gradient reaching the first layer of a 10-layer sigmoid network, and why did people stop using sigmoid in hidden layers?
- ReLU is not differentiable at 0. Why is that not a practical problem for training?
- A ReLU unit whose pre-activation is negative for every training example is "dead". What gradient do its incoming weights receive, and will it come back to life on its own? How does Leaky ReLU change that?
- `d_relu` is the activation's derivative, not the gradient of the loss. How do the two combine in a backward pass?
