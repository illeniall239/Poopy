# Matrix factorization

Topic: 17. Recommender systems basics
Difficulty: 3 of 3

## Problem

Matrix factorization gives every user a vector `p_u` and every item a vector `q_i` of length `n_factors`, and predicts a rating as their dot product `p_u · q_i`. Write a class `MatrixFactorization` with NumPy (allowed) that learns the vectors by gradient descent on the observed ratings only.

- `__init__(self, n_factors: int = 2, lr: float = 0.005, reg: float = 0.01, n_epochs: int = 2000, seed: int = 0)` stores the settings. Raise `ValueError` if `n_factors < 1`.
- `fit(self, ratings: list[tuple[int, int, float]], n_users: int, n_items: int) -> list[float]` trains on `(user, item, rating)` triples, with users numbered `0..n_users-1` and items `0..n_items-1`:
  1. Initialize with `rng = np.random.default_rng(seed)`, then `P = rng.normal(0.0, 0.1, size=(n_users, n_factors))`, then `Q = rng.normal(0.0, 0.1, size=(n_items, n_factors))`.
  2. The loss is `L = Σ (p_u · q_i - r)² + reg · (‖P‖² + ‖Q‖²)`, where the sum runs over the observed triples only and `‖·‖²` is the sum of squared entries.
  3. Each epoch is one full-batch step: compute `∂L/∂P` and `∂L/∂Q` at the current `P` and `Q`, then update both, `P ← P - lr · ∂L/∂P` and `Q ← Q - lr · ∂L/∂Q`.
  4. Return the list of `n_epochs` losses, each computed after that epoch's update.

  Raise `ValueError` if `ratings` is empty or any user or item index is out of range.
- `predict(self, user: int, item: int) -> float` returns `p_user · q_item` as a Python `float`. Raise `RuntimeError` before `fit`.
- `rmse(self, ratings: list[tuple[int, int, float]]) -> float` returns the root mean squared error of `predict` over the given triples.

Cells nobody rated are unknown, not zero: they never enter the loss.

## Examples

```
train, test = planted rank-2 ratings (30 users × 40 items, 80% observed)
mf = MatrixFactorization(n_factors=2, seed=0)
losses = mf.fit(train, 30, 40)       → 2000 losses, falling from about 4750 to about 1.6
mf.rmse(test)                        → well under 0.15 (predicting the mean everywhere: about 0.58)
every observed rating is 4.0         → unobserved cells are also predicted close to 4.0
MatrixFactorization(n_factors=0)     → ValueError
```

## Constraints

- NumPy allowed; no scikit-learn or PyTorch in the solution. Vectorize each epoch: no Python loop over ratings inside the epoch loop.
- Up to 200 users, 200 items and 10 000 ratings; the tests' 2000 epochs on 30 × 40 must take well under 2 seconds.
- The tests check properties (held-out RMSE, falling loss, determinism for a seed, the effect of `reg`), not exact numbers.

## Hints

1. For one observed triple `(u, i, r)` with error `e = p_u · q_i - r`, what is the derivative of `e²` with respect to `p_u`? With respect to `q_i`?
2. If you put all ratings into a dense `n_users × n_items` array `R`, what second array of the same shape stops the unrated cells from contributing any error?
3. With a residual matrix `E` that is zero on unrated cells, which single matrix product gives `Σᵢ eᵤᵢ qᵢ` for every user at once?
4. Why must both gradients be computed before either `P` or `Q` is changed, and what does the `reg` term add to each gradient?

## Explain-back

- What would the model learn if the loss also counted the unrated cells as zeros? Which test catches that?
- How is this the low-rank approximation from Phase 7, and why can you not just run an SVD on the ratings matrix here?
- The held-out RMSE is excellent. Does that prove the top-10 list each user sees is good? What would you measure instead?
- A new user joins with no ratings. What is their vector after training, and what would you show them instead?
