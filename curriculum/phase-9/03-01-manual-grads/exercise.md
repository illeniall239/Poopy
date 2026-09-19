# Gradients by hand

Topic: 3. Computational graphs and backprop by hand
Difficulty: 1 of 3

## Problem

The expression `L = (a*b + c) * f` is a small computational graph with two intermediate nodes:

```
e = a * b
d = e + c
L = d * f
```

Write `manual_grads(a, b, c, f)` in plain Python (no numpy, no torch, no autograd library). It takes four floats and returns a dict with exactly the keys `"a"`, `"b"`, `"c"`, `"f"`, mapping each input to the partial derivative `∂L/∂input` at those values, as floats.

Work it out the way backprop does: start from `∂L/∂L = 1`, and walk the graph backwards, multiplying each node's upstream gradient by the local derivative of the operation. Your answers are checked against a central-difference numeric derivative of `L` within `1e-6`.

## Examples

```
manual_grads(2.0, -3.0, 10.0, -2.0)  → {"a": 6.0, "b": -4.0, "c": -2.0, "f": 4.0}
manual_grads(0.0, 0.0, 0.0, 0.0)     → {"a": 0.0, "b": 0.0, "c": 0.0, "f": 0.0}
manual_grads(1.0, 1.0, 1.0, 1.0)     → {"a": 1.0, "b": 1.0, "c": 1.0, "f": 2.0}
```

## Constraints

- Inputs are finite floats with `|x| ≤ 1000`.
- Plain Python only.

## Hints

1. What are the forward values of `e`, `d` and `L`? You will need some of them on the way back.
2. For `L = d * f`, what is `∂L/∂d` and what is `∂L/∂f`?
3. An addition node `d = e + c` passes its upstream gradient to each input unchanged. Why? What local derivative is it multiplying by?
4. To get `∂L/∂a` you pass through `L`, then `d`, then `e`. Do you add the local derivatives along that path, or multiply them?

## Explain-back

- Along a path, local derivatives are multiplied, not added. Use the chain rule to say why.
- Which forward values did the backward pass need, and why does a real framework store them during the forward pass?
- This function computes gradients; it does not change `a`, `b`, `c` or `f`. What does, in a training loop, and why is "backprop is the learning algorithm" not quite right?
