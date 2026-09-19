# XOR by hand

Topic: 1. The neuron, MLPs and the forward pass
Difficulty: 2 of 3

## Problem

No training here: set the weights yourself. Plain Python, no numpy, no torch.

- `xor_net()` returns `(W1, b1, W2, b2)` for a 2-2-1 network: `W1` has 2 rows of 2 weights (one row per hidden unit), `b1` has 2 biases, `W2` has 1 row of 2 weights, `b2` has 1 bias. All plain floats.
- `predict(x, net)` runs that network on one input `x` (a list of two floats, each 0 or 1): hidden units use ReLU, the output unit has no activation, and the prediction is `1` if the output is greater than `0.5`, else `0`. `net` is the tuple returned by `xor_net()`.

`predict(x, xor_net())` must return the XOR of the two inputs for all four cases.

## Examples

```
predict([0, 0], xor_net())  → 0
predict([0, 1], xor_net())  → 1
predict([1, 0], xor_net())  → 1
predict([1, 1], xor_net())  → 0

A net that is NOT xor_net() still runs through predict:
predict([1, 1], ([[1, 0], [0, 1]], [0, 0], [[1, 1]], [0]))  → 1     output 2 > 0.5
```

## Constraints

- Weights must be finite floats; there is no requirement on their size.
- `predict` must not special-case the inputs: it computes the forward pass.

## Hints

1. Draw the four XOR points on a plane. Can one straight line separate the 1s from the 0s? What does that say about a network with no hidden layer?
2. What does XOR equal in terms of OR and AND: `x1 OR x2` minus something?
3. Can one ReLU unit compute something like `x1 + x2` and another something like `x1 + x2 - 1`? What do those two give for each of the four inputs?
4. With those two hidden activations, which output weights turn `[0, 0]`, `[1, 0]`, `[1, 0]`, `[2, 1]` into `0, 1, 1, 0`?

## Explain-back

- Why can no single-layer network (input straight to one output unit) fit XOR, whatever weights you choose?
- What happens to your network if you replace ReLU by the identity? Does your solution still work? Why not, in terms of what the layers collapse into?
- Your hidden units happen to be interpretable (an OR-like unit and an AND-like unit). Why should you not expect that from a trained network?
- How many parameters does your 2-2-1 network have? Which of them did you actually need to be nonzero?
