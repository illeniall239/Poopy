# Nearest vector

Topic: 2. Vectors, dot product, norms
Difficulty: 2 of 3

## Problem

Write two functions in pure Python (no NumPy):

- `nearest_by_euclidean(query: list[float], vectors: list[list[float]]) -> int` — the index of the vector with the smallest Euclidean distance to `query`.
- `nearest_by_cosine(query: list[float], vectors: list[list[float]]) -> int` — the index of the vector with the largest cosine similarity to `query`.

On a tie, return the smallest index. Raise `ValueError` if `vectors` is empty, if any vector's length differs from the query's, or (cosine only) if the query or any candidate is the zero vector.

The two measures do not always agree; the tests include a case where they pick different neighbors.

Only `math` from the standard library is allowed.

## Examples

```
vectors = [[10.0, 10.0], [1.2, 0.8], [-1.0, -1.0]]
nearest_by_euclidean([1.0, 1.0], vectors)  → 1     distance 0.28 beats 12.7
nearest_by_cosine([1.0, 1.0], vectors)     → 0     [10, 10] points exactly the same way

nearest_by_euclidean([0.0, 0.0], [[1.0, 0.0], [0.0, 1.0]])  → 0     tie, smallest index
nearest_by_cosine([1.0, 0.0], [[0.0, 0.0]])                  → ValueError
nearest_by_euclidean([1.0], [])                              → ValueError
```

## Constraints

- Up to 5 000 candidate vectors of up to 100 entries each; a single pass over the candidates is enough.
- Do not sort the candidates; keep the best index as you go.

## Hints

1. What single number do you need to compute per candidate for each measure, and is "best" the smallest or the largest of it?
2. You need `sqrt` to report a distance. Do you need it to *rank* distances?
3. When two candidates score exactly the same, which comparison operator (`<` or `<=`) keeps the earlier index?
4. Cosine divides by the candidate's norm. When is that division undefined, and should the query's norm be checked once or once per candidate?

## Explain-back

- In the first example the two measures disagree. Describe a real dataset where cosine is the right choice and one where Euclidean is.
- If every vector is first scaled to unit length, do the two measures still disagree? Why or why not?
- Is it true that if `a` is the cosine-nearest to `q`, then `a` is also the Euclidean-nearest? Point to the example that refutes it.
- Why is comparing squared distances enough to find the nearest, and why would comparing raw dot products *not* be enough for cosine?
