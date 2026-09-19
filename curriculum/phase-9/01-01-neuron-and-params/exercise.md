# Neuron and parameter count

Topic: 1. The neuron, MLPs and the forward pass
Difficulty: 1 of 3

## Problem

Write two functions in plain Python (no numpy, no torch).

- `neuron(x, w, b, act)` computes one artificial neuron: the weighted sum of the inputs `x` with the weights `w`, plus the bias `b`, passed through the activation function `act`. `x` and `w` are lists of floats of the same length; `act` is any function from float to float. Raise `ValueError` if the lengths differ.
- `count_params(layer_sizes)` returns how many learnable numbers an MLP has when every layer is fully connected with a bias. `layer_sizes` lists the width of every layer starting with the input, so `[2, 2, 1]` is a 2-input, 2-hidden, 1-output network. An input layer alone has no parameters.

## Examples

```
neuron([1.0, 2.0], [0.5, -1.0], 0.25, lambda z: z)        → -1.25
neuron([1.0, 2.0], [0.5, -1.0], 0.25, lambda z: max(0, z)) → 0.0
neuron([], [], 3.0, lambda z: z)                          → 3.0
count_params([2, 2, 1])                                   → 9       (2*2 + 2) + (2*1 + 1)
count_params([784, 128, 10])                              → 101770
count_params([5])                                         → 0
```

## Constraints

- Lists have at most 10 000 entries.
- `layer_sizes` has 1 to 20 widths, each between 1 and 10 000.
- Plain Python only.

## Hints

1. What are the three parts of a neuron, and in which order are they applied?
2. Which built-in lets you walk two lists in lock-step?
3. For one fully connected layer from `n_in` units to `n_out` units, how many weights does each output unit own, and how many biases does the layer add?
4. How can you visit every consecutive pair of `layer_sizes` in one loop?

## Explain-back

- Why is the bias not optional when counting parameters? What would a layer without a bias be unable to represent?
- If you stack two layers with the identity activation, how many parameters do they have and how many does the single linear layer they collapse into have?
- Does a hidden unit in a trained MLP "detect" something you could name? Why should you be careful with that reading?
- Does doubling the depth of a network always make it better? What does it always make it?
