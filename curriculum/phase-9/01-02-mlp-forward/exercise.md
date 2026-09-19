# MLP forward pass

Topic: 1. The neuron, MLPs and the forward pass
Difficulty: 2 of 3

## Problem

Write `mlp_forward(x, layers)` in plain Python (no numpy, no torch).

`x` is one input as a list of floats. `layers` is a list of `(W, b, act)` triples, applied in order. In each triple, `W` is a list of rows, one row per output unit, each row holding one weight per input unit (so a layer from 3 inputs to 2 outputs has `W` with 2 rows of 3 numbers); `b` is a list with one bias per output unit; `act` is a function from float to float applied to every output unit. The output of one layer is the input of the next. Return the final layer's output as a list of floats.

Raise `ValueError` if a layer's row length does not match the number of values flowing into it.

## Examples

```
identity = lambda z: z
relu = lambda z: max(0.0, z)

mlp_forward([1.0, 2.0], [([[1.0, 1.0], [1.0, -1.0]], [0.0, 0.5], relu)])
    → [3.0, 0.0]                  unit 0: 1+2+0 = 3; unit 1: 1-2+0.5 = -0.5 → relu → 0

mlp_forward([1.0, 2.0], [
    ([[1.0, 1.0], [1.0, -1.0]], [0.0, 0.5], relu),
    ([[2.0, -1.0]], [1.0], identity),
])
    → [7.0]                       2*3 - 1*0 + 1
```

## Constraints

- At most 10 layers, each at most 100 wide.
- Plain Python only; you may reuse the idea of `neuron` from the previous exercise.

## Hints

1. What does one row of `W` together with one entry of `b` describe?
2. If you already have a function for one neuron, what does one layer look like in terms of it?
3. After computing a layer's output, what becomes the `x` for the next layer?
4. Where is the only place a shape mismatch can be detected, and what two lengths do you compare?

## Explain-back

- With `identity` as every activation, show on paper that two layers `(W2, b2)` after `(W1, b1)` equal a single layer. What are its weights and bias?
- What is the shape of `W` for a layer from `n_in` to `n_out` units, and why does a batch of inputs become a matrix with one row per example?
- Why does the universal approximation theorem not tell you how to train the network or how wide it needs to be?
- Is the activation applied before or after adding the bias? What changes if you swap them?
