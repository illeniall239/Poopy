# Dot product and norms

Topic: 2. Vectors, dot product, norms
Difficulty: 1 of 3

## Problem

Write three functions over vectors given as `list[float]`, in pure Python (no NumPy):

- `dot(a: list[float], b: list[float]) -> float` — the sum of elementwise products.
- `norm(v: list[float], p: int = 2) -> float` — the L1 norm (sum of absolute values) when `p == 1`, the L2 norm (square root of the sum of squares) when `p == 2`. Raise `ValueError` for any other `p`.
- `cosine_similarity(a: list[float], b: list[float]) -> float` — `dot(a, b) / (|a| |b|)` with L2 norms.

`dot` and `cosine_similarity` raise `ValueError` when the two vectors have different lengths. `cosine_similarity` raises `ValueError` if either vector has norm 0, because the similarity is undefined there.

Only `math` from the standard library is allowed.

## Examples

```
dot([1, 2, 3], [4, 5, 6])          → 32.0
dot([1, 0], [0, 1])                → 0.0          orthogonal
norm([3, 4])                       → 5.0
norm([3, -4], p=1)                 → 7.0
cosine_similarity([1, 1], [2, 2])  → 1.0          same direction, different length
cosine_similarity([1, 0], [0, 1])  → 0.0
cosine_similarity([1, 0], [-1, 0]) → -1.0
dot([1, 2], [1])                   → ValueError
cosine_similarity([0, 0], [1, 2])  → ValueError
```

## Constraints

- Vectors have 1 to 10 000 entries.
- Results must match NumPy within `1e-9`; `cosine_similarity` must stay inside `[-1, 1]` up to rounding.

## Hints

1. Which built-in pairs `a[i]` with `b[i]` so you can write the dot product without indexing?
2. `norm([3, 4])` is `5`. Which two operations does that number come from, and in which order?
3. What is `dot(v, v)` in terms of `norm(v)`? Can you reuse one function inside the other?
4. Before dividing in `cosine_similarity`, what value of a norm would make the answer meaningless rather than merely wrong?

## Explain-back

- `[1, 2] * [3, 4]` elementwise is `[3, 8]`; the dot product is `11`. In one sentence each, what does each tell you about the two vectors?
- `cosine_similarity([1, 1], [100, 100])` is `1.0`. Are the vectors identical? What does cosine similarity ignore that Euclidean distance keeps?
- Is `norm(a) - norm(b)` the same as `norm(a - b)`? Give a two-entry counterexample.
- Why does the L1 norm of `[3, -4]` need `abs`, but the L2 norm does not?
