# Linear layer backward

Topic: 6. Vectorized backprop: tensors and the backprop ninja
Difficulty: 2 of 3

## Problem

A linear layer computes `Y = X @ W + b` for a whole batch at once: `X` has shape `(N, D)` (one example per row), `W` has shape `(D, M)`, `b` has shape `(M,)` and is broadcast over the `N` rows, so `Y` has shape `(N, M)`.

Write `linear_backward(X, W, dY)` in NumPy. `dY` is the gradient of some scalar loss with respect to `Y` (shape `(N, M)`). Return the tuple `(dX, dW, db)`: the gradients of that same loss with respect to `X`, `W` and `b`, as NumPy arrays with exactly the shapes of `X`, `W` and `b`: `(N, D)`, `(D, M)` and `(M,)`. The bias value itself is not needed, so it is not an argument.

- Vectorized: no Python loops over rows or columns.
- Do not modify the input arrays.
- Raise `ValueError` if `X`, `W` or `dY` is not 2-D, or if the shapes do not fit together (`X.shape[1] != W.shape[0]`, or `dY.shape != (N, M)`).

The tests check your gradients against central finite differences of the forward pass, so they must be exact, not just the right shape.

## Examples

```
X  = [[1, 2]]            (N=1, D=2)
W  = [[1, 0, 2],
      [0, 1, 3]]         (D=2, M=3)
dY = [[1, 1, 1]]
linear_backward(X, W, dY) → dX = [[3, 4]]
                            dW = [[1, 1, 1],
                                  [2, 2, 2]]
                            db = [1, 1, 1]

Two identical rows: every gradient that sums over the batch doubles.
linear_backward([[1, 2], [1, 2]], W, [[1, 1, 1], [1, 1, 1]])
    → dX = [[3, 4], [3, 4]], dW = [[2, 2, 2], [4, 4, 4]], db = [2, 2, 2]
```

## Constraints

- NumPy only; no torch, no autograd.
- `N`, `D`, `M` up to 1000.
- Results match finite differences within `1e-6`.

## Hints

1. Write one entry of `Y` as a sum: `Y[n, m] = Σ_d X[n, d] W[d, m] + b[m]`. Which entries of `Y` does `W[d, m]` touch, and which does `X[n, d]` touch?
2. For each gradient, which matrix product of `X`, `W` and `dY` has the right shape? Is there only one way to get that shape?
3. The bias `b[m]` was copied into every row of `Y`. When one value is used `N` times, how do the `N` gradient contributions combine?
4. If `D == M`, the shapes line up whether you transpose `W` or not. What small example would tell `dY @ W` apart from `dY @ W.T`?

## Explain-back

- If `W` is square, `dY @ W` and `dY @ W.T` have the same shape. Why does matching shapes not prove a gradient is right, and how does finite-difference checking catch it?
- Why is `db` a sum over the batch axis and not a mean or a single row? What would happen to training if you returned `dY[0]`?
- If the loss is a mean over the batch, where does the `1/N` enter: in `dY`, or inside `linear_backward`? What goes wrong if you apply it in both places?
- Why is `dW = X.T @ dY` the sum of one outer product per example?
