# Broadcast shape

Topic: 3. Matrices, matrix multiplication and broadcasting
Difficulty: 2 of 3

## Problem

Write `broadcast_shape(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]` that applies NumPy's broadcasting rules to two shape tuples and returns the shape of the result, without building any arrays.

The rules:

1. Align the two shapes from the right. The shorter one is padded on the left with 1s until both have the same length.
2. Walk the aligned dimensions in pairs. Two sizes are compatible when they are equal or one of them is 1; the result takes the larger.
3. If any pair is incompatible, raise `ValueError`.

A 0-d shape `()` broadcasts with anything and returns the other shape.

Pure Python only (no NumPy in the solution; the test uses NumPy to confirm your answers).

## Examples

```
broadcast_shape((3, 4), (4,))        → (3, 4)      a row vector reaches every row
broadcast_shape((3, 1), (1, 4))      → (3, 4)      both stretch
broadcast_shape((3,), (3, 1))        → (3, 3)      the silent bug
broadcast_shape((2, 1, 5), (7, 1))   → (2, 7, 5)
broadcast_shape((), (6, 2))          → (6, 2)
broadcast_shape((3,), (4,))          → ValueError
broadcast_shape((2, 3), (3, 2))      → ValueError
```

## Constraints

- Shapes have 0 to 6 dimensions, every size between 1 and 1000.
- The answer must equal `np.broadcast_shapes(a, b)` for every valid pair and raise exactly when NumPy raises.
- Return a `tuple`, not a list.

## Hints

1. Which end of the two tuples lines up first? What does that say about padding: does the 1 go on the left or the right?
2. After padding, both tuples have the same length. Which built-in lets you walk them in pairs?
3. For one pair `(p, q)`, write down every case: equal, one is 1, neither. What does each produce?
4. `(3,)` against `(3, 1)`: after padding `(3,)` becomes `(1, 3)`. Walk the pairs by hand. Is the result what you expected?

## Explain-back

- Why does a `(3,)` bias added to a `(3, 1)` column give a `(3, 3)` matrix instead of an error? How would you spot this bug in a real program?
- Broadcasting is often described as "copying the small array". Does NumPy actually allocate the copies? What would that cost for a `(10000, 10000)` matrix plus a row?
- `X` is `(n, d)` and `w` is `(d,)`. Is `X + w` broadcasting or matmul? What about `X @ w`, and what shape does each produce?
- Can broadcasting ever shrink a dimension? Why must the result be at least as large as both inputs in every dimension?
