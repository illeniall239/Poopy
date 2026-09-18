# Power iteration

Topic: 14. Eigenvectors and SVD, just enough for PCA
Difficulty: 2 of 3

## Problem

Write two functions with NumPy (required) for a symmetric matrix `A` of shape `(n, n)`:

- `power_iteration(A: np.ndarray, n_iter: int = 1000, tol: float = 1e-12, seed: int = 0) -> tuple[float, np.ndarray]` — start from `np.random.default_rng(seed).normal(size=n)` (a fixed start such as all-ones can be exactly orthogonal to the eigenvector you want, and then the iteration never moves), repeatedly set `v = A v / ‖A v‖`, and stop when `‖v_new - v‖ < tol` or after `n_iter` iterations. Return `(eigenvalue, v)` with the eigenvalue as the Rayleigh quotient `vᵀ A v` (for a unit `v`) and `v` a unit vector. Raise `ValueError` if `A` is not square 2-D or is not symmetric within `1e-9`.
- `top_two_eigenpairs(A: np.ndarray, n_iter: int = 1000) -> tuple[tuple[float, np.ndarray], tuple[float, np.ndarray]]` — the dominant pair by `power_iteration`, then one deflation step: run `power_iteration` on `A - λ₁ v₁ v₁ᵀ` to get the second pair. Return `((λ₁, v₁), (λ₂, v₂))`.

Eigenvectors are only defined up to sign: the test compares `|vᵀ v_numpy|` to 1, never `v` itself.

## Examples

```
A = np.array([[2.0, 0.0], [0.0, 1.0]])
power_iteration(A)          → (2.0, [±1, 0])
A = np.array([[2.0, 1.0], [1.0, 2.0]])
power_iteration(A)          → (3.0, ±[0.7071, 0.7071])
top_two_eigenpairs(A)       → ((3.0, ±[0.7071, 0.7071]), (1.0, ±[0.7071, -0.7071]))
power_iteration(np.array([[1.0, 2.0], [0.0, 1.0]]))   → ValueError   not symmetric
```

## Constraints

- `n` up to 200; a few thousand matrix–vector products at most.
- Eigenvalues within `1e-6` of `np.linalg.eigh`, `|vᵀ v_numpy| > 1 - 1e-6`, and `A v ≈ λ v` within `1e-6`.
- The test matrices are symmetric positive semi-definite with a clear gap between the top eigenvalues, so the iteration converges.

## Hints

1. Write `v` as a combination of eigenvectors `Σ cᵢ uᵢ`. What is `Aᵏ v`? Which term wins as `k` grows, and how fast do the others shrink relative to it?
2. Why normalize every iteration rather than only at the end? What happens to `‖Aᵏ v‖` after 1000 steps with `λ₁ = 10`?
3. Given a unit eigenvector `v`, what is `vᵀ A v`? Why is that a better eigenvalue estimate than the ratio of one component?
4. After deflation, what does `(A - λ₁ v₁ v₁ᵀ)` do to `v₁`? What is its eigenvalue for `v₁` now, and why does power iteration then find `v₂`?

## Explain-back

- A test compares your eigenvector to NumPy's with `assert_allclose` and fails by a sign. Is your code wrong? How should eigenvectors be compared?
- Why does power iteration find only the largest-magnitude eigenvalue? What breaks when `λ₁ = -λ₂`?
- PCA's first component is the top eigenvector of the covariance matrix. In terms of the data cloud, what direction is that and what does `λ₁` measure?
- `np.linalg.eigh` returns eigenvalues in ascending order. Which index is the first principal component, and what mistake does that ordering invite?
