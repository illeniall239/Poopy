# Vectorized minibatch SGD

Topic: 3. Gradient descent for linear regression
Difficulty: 3 of 3

## Problem

Train multi-feature linear regression `ŷ = X w + b` with minibatch stochastic gradient descent in NumPy, and check it against the closed form. `X` has shape `(n, d)` and `y` shape `(n,)`; features may live on wildly different scales (one in thousands, one in hundredths).

- `normal_equation(X: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, float]` — prepend a column of ones to `X` to get `A`, solve `(AᵀA) θ = Aᵀy` with `np.linalg.solve` (never an explicit inverse), and return `(θ[1:], θ[0])` as `(w, b)` with `w` of shape `(d,)` and `b` a `float`.
- `sgd_linreg(X: np.ndarray, y: np.ndarray, lr: float, epochs: int, batch_size: int, seed: int) -> tuple[np.ndarray, float, list[float]]`:
  1. Standardize: `mu = X.mean(axis=0)`, `sigma = X.std(axis=0)` (population std), `Z = (X − mu) / sigma`.
  2. Start from `w_z = zeros(d)`, `b_z = 0.0`, and make `rng = np.random.default_rng(seed)`.
  3. Every epoch, draw a new order `rng.permutation(n)` and walk it in consecutive batches of `batch_size` rows (the last may be shorter). For a batch of `m` rows, with `err = Z_batch @ w_z + b_z − y_batch`, step `w_z -= lr · (2/m) · Z_batchᵀ err` and `b_z -= lr · (2/m) · Σ err`. One matrix product per step; no Python loop over rows.
  4. After each epoch append the MSE over all `n` rows to `loss_history` (so it has `epochs` entries).
  5. Convert back to the original units: `w = w_z / sigma`, `b = b_z − Σ (w_z · mu / sigma)`. Return `(w, b, loss_history)` with `b` a `float`.

Raise `ValueError` if `X` is not 2-D, `y` is not 1-D, their row counts differ, `n == 0`, or any column of `X` is constant (`sigma == 0`), in either function where it applies (`normal_equation` needs the shape checks only).

On noiseless linear data `sgd_linreg` reaches the normal-equation `(w, b)` to within `1e-6` relative in 30 epochs at `lr = 0.05`; on noisy data it lands close to it and its final loss is within 1% of the closed-form MSE.

## Examples

```
X = [[1000, 0.01], [2000, 0.05], [1500, 0.02], [3000, 0.03], [2500, 0.04], [500, 0.02]]
y = 0.002·x₀ + 100·x₁ + 1 for each row
normal_equation(X, y)                       → (w ≈ [0.002, 100.0], b ≈ 1.0)
sgd_linreg(X, y, 0.05, 30, 2, seed=0)       → (w ≈ [0.00199, 100.3], b ≈ 0.9996, 30 losses)   still converging
sgd_linreg(X, y, 0.05, 3000, 2, seed=0)     → (w ≈ [0.002, 100.0], b ≈ 1.0, 3000 losses)
the same loop on the raw, unscaled X         → the loss overflows to inf / nan within a few steps
```

## Constraints

- NumPy only; `n` up to 5 000, `d` up to 20; the tests' runs take well under a second.
- `loss_history[-1]` is the MSE of the returned `(w, b)` on `(X, y)`.
- Results are deterministic for a given `seed`.

## Hints

1. Write the MSE for a batch in matrix form. What shape is `Z_batchᵀ err`, and why does it hold the gradient for every weight at once?
2. With one feature around 1 000 and another around 0.01, how do the two components of the gradient compare, and what learning rate would suit both?
3. After standardizing, the model is `ŷ = ((x − mu) / sigma) · w_z + b_z`. Expand it: which coefficient multiplies the raw `x`, and what constant is left over?
4. If every epoch walked the rows in the same order, what would two runs with different seeds produce, and what systematic bias could a fixed order add?

## Explain-back

- Why does SGD on standardized features land on the same answer as the normal equations, and why is it not bit-for-bit identical on noisy data?
- A tutorial's `lr = 0.05` works on its data and your loss becomes `nan` after three steps. What happened, and what is the fix that is not "make the learning rate tiny"?
- `mu` and `sigma` here come from the data being trained on. When you later predict for new rows, which `mu` and `sigma` must you use, and why?
- When would you choose SGD over the closed form for linear regression, given the closed form exists?
