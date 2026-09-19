# Gradient highway

Topic: 14. Modern CNN ideas: residual connections and transfer learning
Difficulty: 2 of 3

## Problem

Backprop through a stack of layers multiplies their local derivatives. When those derivatives are small, the product shrinks towards zero with depth and early layers stop learning. A residual layer `h + F(h)` has local derivative `1 + F'(h)` instead of `F'(h)`. Show both effects.

- `chain_grad(derivs, residual)` in plain Python: `derivs` is a list of the local derivatives `d_1 … d_n` of a chain of scalar layers. Return the derivative of the whole chain: `d_1 · d_2 · … · d_n` when `residual` is `False`, and `(1 + d_1) · (1 + d_2) · … · (1 + d_n)` when it is `True`. An empty chain has derivative `1.0`. Return a float.
- `input_grad_norm(depth, width, residual, seed)` with PyTorch, following this recipe exactly:
  1. `torch.manual_seed(seed)`.
  2. Draw `depth` weight matrices in order, each `torch.randn(width, width) * 0.5 / math.sqrt(width)`.
  3. Then draw the input `x = torch.randn(1, width)` and make it require a gradient.
  4. `h = x`. For each weight `W` in order: `z = torch.tanh(h @ W.T)`; then `h = h + z` if `residual`, else `h = z`.
  5. Backpropagate `h.sum()` and return the L2 norm of `x`'s gradient as a Python float.

  With `depth = 0` the gradient is all ones, so the norm is `sqrt(width)`. Raise `ValueError` if `depth < 0` or `width < 1`.

## Examples

```
chain_grad([0.5, 0.5, 0.5], residual=False)  → 0.125
chain_grad([0.5, 0.5, 0.5], residual=True)   → 3.375
chain_grad([0.1] * 50, residual=False)       → 1e-50      vanished
chain_grad([], residual=False)               → 1.0
input_grad_norm(0, 16, False, 0)             → 4.0
input_grad_norm(50, 16, False, 0)            → about 1e-16   plain stack: vanished
input_grad_norm(50, 16, True, 0)             → about 20      residual stack: alive
```

## Constraints

- `depth` is at most 100, `width` at most 64; CPU only.
- The tests check exact values (within `1e-5` relative) for shallow stacks, so follow the drawing order above.

## Hints

1. What is the derivative of `f(g(x))` in terms of `f'` and `g'`? What does that become for a chain of fifty layers?
2. What is `0.1^50`? What is `1.1^50`? What does that say about where the residual form keeps the product?
3. In the torch recipe, what is the derivative of `h + tanh(h @ W.T)` with respect to `h` when `W` is small?
4. After `backward`, where does PyTorch put the gradient of the input, and which tensor method gives its L2 norm?

## Explain-back

- Why does the product of fifty local derivatives each below 1 vanish, and which layers of a plain deep net suffer first?
- The residual derivative is `1 + F'`. Why does the `1` make gradient flow through a deep stack robust even when `F'` is tiny?
- Can residual products explode instead? What else in a ResNet keeps the scale in check?
- Transformers stack dozens of blocks. Where does the same `1 + F'` argument apply there?
