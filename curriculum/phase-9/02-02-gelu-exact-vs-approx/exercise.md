# GELU: exact vs tanh approximation

Topic: 2. Activation functions
Difficulty: 1 of 3

## Problem

GELU (the activation in BERT and GPT-2) weights its input by how likely a standard normal variable is to be below it: `GELU(x) = x · Φ(x)`, where `Φ` is the standard normal CDF. Early implementations used a cheaper tanh approximation, and some checkpoints still depend on which one was used. Write both in plain Python (the `math` module is fine; no numpy, no torch).

- `gelu_exact(x)` = `0.5 · x · (1 + erf(x / √2))`, using `math.erf`.
- `gelu_tanh(x)` = `0.5 · x · (1 + tanh(√(2/π) · (x + 0.044715 · x³)))`, using `math.tanh`.

Both take one float and return a float. They must agree within `5e-4` for every `x` in `[-8, 8]` but are not identical: `gelu_tanh` must follow the formula above within `1e-12`, it may not just call `gelu_exact`. Neither may raise for `|x|` up to `1e6`: for large positive `x` both return about `x`, for large negative `x` both return about `0`.

## Examples

```
gelu_exact(0.0)    → 0.0
gelu_exact(1.0)    → 0.8413447460685429
gelu_tanh(1.0)     → 0.8411919906082768      differs from exact in the 4th decimal
gelu_exact(-1.0)   → -0.15865525393145707    negative outputs are allowed, unlike ReLU
gelu_exact(-3.0)   → -0.0040496940948904
gelu_tanh(1e6)     → 1000000.0
```

## Constraints

- Inputs are finite floats with `|x| ≤ 1e6`.
- Plain Python and `math` only.

## Hints

1. How do you get the standard normal CDF `Φ(x)` out of `math.erf`? What is the argument scaling?
2. Where does the approximation formula's `tanh` come from: which curve is it trying to imitate?
3. For `x = 1e6`, what is `x³`, and does Python's `math.tanh` overflow on a huge argument or simply saturate?
4. To check the two agree, which `x` values would you try? Where do you expect the gap to be largest: near 0, around `|x| ≈ 2`, or far out?

## Explain-back

- GELU is negative for moderately negative inputs and has a nonzero gradient there. How does that change the "dead unit" story compared with ReLU?
- The two versions differ by at most about `5e-4`. When would that difference matter (think of loading pretrained weights), and when would it not?
- Why is GELU a hidden-layer activation while softmax is only ever an output activation?
