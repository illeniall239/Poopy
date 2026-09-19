# Residual block

Topic: 14. Modern CNN ideas: residual connections and transfer learning
Difficulty: 1 of 3

## Problem

A residual block computes `x + F(x)`: the input skips past the layers `F` and is added back to their output. Write it twice.

- `residual_block_forward(x, f)` in plain Python: `x` is a list of floats and `f` is any function from a list of floats to a list of floats. Return a new list `[x_i + f(x)_i]`. Call `f` exactly once. Raise `ValueError` if `f(x)` has a different length from `x`.
- `ResidualMLP(dim, hidden)`, an `nn.Module`. Its attribute `f` is `nn.Sequential(nn.Linear(dim, hidden), nn.ReLU(), nn.Linear(hidden, dim))`. `forward(x)` takes a tensor of shape `(B, dim)` and returns `x + self.f(x)`, the same shape. The addition is the **last** operation: there is no activation after it, so the block can pass negative values of `x` straight through.

## Examples

```
residual_block_forward([1.0, -2.0], lambda v: [0.5, 0.5])   → [1.5, -1.5]
residual_block_forward([1.0, -2.0], lambda v: [0.0, 0.0])   → [1.0, -2.0]    F = 0 gives the identity
residual_block_forward([1.0], lambda v: [1.0, 2.0])         → ValueError

block = ResidualMLP(4, 8)
block(x).shape                          → (B, 4)
block(x) equals x + block.f(x)          (to 1e-6)
with every weight and bias of block.f set to zero: block(x) equals x, and d(block(x).sum())/dx is all ones
```

## Constraints

- `dim` and `hidden` are between 1 and 256.
- Use `torch.nn` layers for `ResidualMLP`; plain Python for `residual_block_forward`.

## Hints

1. If `F` has learned nothing useful and outputs zeros, what does the block output? How does that compare with a plain layer that outputs zeros?
2. How do you add two lists elementwise without calling `f` twice?
3. In `ResidualMLP`, which tensor must you keep a reference to before running `self.f`?
4. Take the derivative of `x + F(x)` with respect to `x`. Which term is there no matter what `F`'s weights are?

## Explain-back

- Why does the `+ x` term let gradients reach early layers even when `F`'s derivative is tiny?
- Why does a plain 50-layer network often train worse, even on the training set, than a 20-layer one, while a 50-layer ResNet does not?
- Why is the block easy to initialize as (nearly) the identity, and why is that a good starting point for a deep stack?
- Where else will you meet `x + F(x)`? (Hint: every transformer layer has two of them.)
