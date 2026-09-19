# Unbroadcast

Topic: 6. Vectorized backprop: tensors and the backprop ninja
Difficulty: 2 of 3

## Problem

When NumPy (or PyTorch) broadcasts an array of shape `shape` up to a bigger shape, every value is reused along the broadcast axes. In the backward pass the gradient arrives with the big shape and must be brought back to `shape`: each reused value collects the **sum** of the gradients of all its copies.

Write `unbroadcast(grad, shape)` in NumPy. `grad` is an array; `shape` is a tuple that broadcasts to `grad.shape` under NumPy's rules (align on the right; each dimension of `shape` is either equal to the matching dimension of `grad` or `1`; `shape` may have fewer dimensions). Return an array of exactly `shape`:

- sum over the leading axes that `shape` does not have at all;
- sum, keeping the axis, over every axis where `shape` has `1` and `grad` does not.

`shape == ()` (a scalar was broadcast) returns a 0-d array holding the total sum. If `shape` already equals `grad.shape`, return an equal array. Do not modify `grad`.

Raise `ValueError` if `shape` cannot broadcast to `grad.shape`: more dimensions than `grad`, or a dimension that is neither `1` nor equal to `grad`'s.

## Examples

```
g = [[1, 2, 3],
     [4, 5, 6]]              shape (2, 3)
unbroadcast(g, (3,))     → [5, 7, 9]
unbroadcast(g, (1, 3))   → [[5, 7, 9]]
unbroadcast(g, (2, 1))   → [[6], [15]]
unbroadcast(g, ())       → 21            (0-d array)
unbroadcast(g, (2, 3))   → g
unbroadcast(np.ones((4, 2, 3)), (2, 1)) → [[12], [12]]
unbroadcast(g, (2,))     → ValueError    (2 does not match 3 on the right)
```

## Constraints

- NumPy only.
- `grad` has at most 6 dimensions and 1 000 000 elements.

## Hints

1. Take `b` of shape `(3,)` added to `X` of shape `(2, 3)`. How many times is each `b[j]` used, and what does the chain rule do with several uses of one value?
2. Broadcasting aligns shapes on the right. How many leading axes does `grad` have that `shape` does not, and what should happen to them?
3. After those leading axes are gone, which remaining axes have size `1` in `shape` but not in `grad`? Which `sum` argument keeps such an axis instead of dropping it?
4. How do you check, before summing anything, that `shape` really could have been broadcast to `grad.shape`?

## Explain-back

- Why is the backward of a broadcast a sum and not a mean, or just taking one slice?
- What does `unbroadcast` do for the bias of a linear layer, and how does that connect to `db = dY.sum(axis=0)`?
- Why are `(3,)` and `(1, 3)` different targets even though they hold the same numbers?
- If an autograd engine skipped the unbroadcast step, what error or silent bug would you expect when it adds a `(3,)` gradient into a `(2, 3)` one?
