# RNN forward pass

Topic: 18. Sequence modeling: n-gram LM → MLP LM → RNN, LSTM, GRU
Difficulty: 2 of 3

## Problem

A vanilla RNN reads a sequence one step at a time and keeps a hidden state that summarizes what it has seen. At every step it applies the **same** weights:

```
h_t = tanh(Wxh · x_t + Whh · h_{t−1} + b)
```

Write `rnn_forward(xs, h0, Wxh, Whh, b)` in plain Python (no numpy, no torch):

- `xs` is the input sequence: a list of `T` vectors, each a list of `D` floats.
- `h0` is the initial hidden state: a list of `H` floats.
- `Wxh` is `H` rows of `D` floats, `Whh` is `H` rows of `H` floats, `b` is `H` floats. Matrix times vector means: output entry `i` is the dot product of row `i` with the vector.

Return the list of hidden states `[h_1, …, h_T]` (each a list of `H` floats), not including `h0`. An empty sequence returns `[]`.

Raise `ValueError` if any `x_t` has a length other than `D` (the row length of `Wxh`), or if `h0`, `b`, `Whh` or the number of rows of `Wxh` disagree on `H`.

## Examples

```
rnn_forward([[1.0], [0.0], [0.0]], [0.0], [[1.0]], [[0.5]], [0.0])
  → [[0.76159...], [0.36340...], [0.17970...]]
      h1 = tanh(1)        h2 = tanh(0.5 · 0.7616)        h3 = tanh(0.5 · 0.3634)

rnn_forward([], [0.3, -0.2], [[1.0], [2.0]], [[0.0, 0.0], [0.0, 0.0]], [0.0, 0.0])  → []
rnn_forward([[1.0, 2.0]], [0.0], [[1.0]], [[1.0]], [0.0])                            → ValueError
```

The input at step 1 still shows up at step 3, but fainter every step: nothing forces the RNN to keep it.

## Constraints

- `T`, `D`, `H` at most 50.
- Plain Python only; the test compares against `torch.nn.RNN` with the same weights.

## Hints

1. At step `t`, which two vectors go into the new hidden state, and where does the second one come from at `t = 1`?
2. Can you write a tiny helper for "matrix times vector" on lists so the step formula reads like the maths?
3. What variable must you overwrite at the end of each step, and what list do you append to?
4. Which checks can you do once before the loop, and which must happen for each `x_t`?

## Explain-back

- The same `Wxh`, `Whh` and `b` are used at every step. What does that buy you (think parameter count and sequence length), and what would go wrong with separate weights per position?
- In the example the first input's trace shrinks by about half each step. What happens to its influence after 50 steps, and what does that say about "RNNs remember everything"?
- During backprop through time the gradient flows back through `Whh` once per step. Why does that make gradients vanish or explode over long sequences?
- Why can this loop not be parallelized across time steps, and how does that motivate attention?
