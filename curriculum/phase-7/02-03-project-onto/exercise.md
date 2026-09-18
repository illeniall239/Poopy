# Project onto

Topic: 2. Vectors, dot product, norms
Difficulty: 2 of 3

## Problem

Write `project(a: list[float], b: list[float]) -> tuple[list[float], list[float]]` in pure Python (no NumPy).

Return `(parallel, orthogonal)`: `parallel` is the projection of `a` onto `b`, the part of `a` that points along `b`; `orthogonal` is what is left, `a - parallel`. Together they must add back up to `a`, and `orthogonal` must have a zero dot product with `b`.

Raise `ValueError` if the lengths differ or if `b` is the zero vector (there is no direction to project onto).

Only `math` from the standard library is allowed.

## Examples

```
project([3, 4], [1, 0])      → ([3.0, 0.0], [0.0, 4.0])
project([3, 4], [2, 0])      → ([3.0, 0.0], [0.0, 4.0])      same direction, same projection
project([1, 1], [1, 1])      → ([1.0, 1.0], [0.0, 0.0])      a already lies along b
project([1, 0], [0, 1])      → ([0.0, 0.0], [1.0, 0.0])      orthogonal: nothing to project
project([2, 2], [-1, 0])     → ([2.0, -0.0], [0.0, 2.0])     projection can point against b
project([1, 2], [0, 0])      → ValueError
```

## Constraints

- Vectors have 1 to 1 000 entries.
- `parallel + orthogonal == a` and `dot(orthogonal, b) == 0` within `1e-9`.
- The projection's length must not depend on the length of `b`, only on its direction.

## Hints

1. The projection of `a` onto `b` is `b` scaled by some number. In terms of dot products, what is that number? Why does it divide by `b·b` and not by `|b|`?
2. Once you have `parallel`, how do you get `orthogonal` with a single elementwise operation?
3. Check `project([3, 4], [2, 0])` by hand. If your scale factor were `a·b / |b|` instead, what would you get, and why is that wrong?
4. Which value of `b` makes the scale factor's denominator zero?

## Explain-back

- Why is `dot(orthogonal, b)` always zero? Show it algebraically from the scale factor.
- `|parallel|` equals `|a| cos θ`. Where does the cosine come from, and what does a negative `|a| cos θ` mean geometrically?
- The two components add up to `a`, and `|a|² = |parallel|² + |orthogonal|²`. Which theorem is that, and why does it need the two parts to be orthogonal?
- Least squares will project a target vector onto the column space of a matrix. How is that the same idea as this exercise with more than one `b`?
