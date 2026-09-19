# Value: the full set of operations

Topic: 4. A scalar autograd engine (micrograd)
Difficulty: 2 of 3

## Problem

Grow your `Value` class into one that can express a neural network and its loss. Write the whole class in this file, in plain Python (the `math` module is fine; no numpy, no torch). You may start by copying your solution to the previous exercise.

**Carried over from the previous exercise:**

- `Value(data, _children=(), _op="")` stores `self.data`, sets `self.grad = 0.0`, and remembers its children and a backward step (a no-op for leaves).
- `a + b`, `a * b` and `a.tanh()` return new `Value`s; a plain `int`/`float` operand is wrapped in a `Value` first.
- `out.backward()` sets `out.grad = 1.0`, orders every value reachable from `out` topologically and runs each backward step in reverse order. Backward steps **add** into children's `grad` (`+=`).

**New:**

- `a ** k` where `k` is a plain `int` or `float` (not a `Value`): value `a.data ** k`. Raise `TypeError` if `k` is anything else.
- `a.exp()`: value `e ** a.data`.
- `a.relu()`: value `max(0, a.data)`; its local derivative is `1` when `a.data > 0` and `0` otherwise (including at exactly 0).
- `-a`, `a - b` and `a / b`. Build these from operations you already have (`-a` as `a * -1`, `a - b` as `a + (-b)`, `a / b` as `a * b ** -1`) rather than writing new backward steps.
- Reflected operations, so a plain number on the **left** works: `2 + a`, `2 * a`, `2 - a` and `2 / a` all return `Value`s with the right value and gradient.

Every operation is checked by a numeric-gradient harness: for an expression built from `Value`s, each input's `grad` after `backward()` must match a central-difference derivative within `1e-6`.

## Examples

```
a = Value(3.0)
(a ** 2).data                   → 9.0
(2 - a).data                    → -1.0
(1 / a).data                    → 0.3333333333333333
(a - a).backward(); a.grad      → 0.0     (fresh a: both uses cancel)

a = Value(2.0); (a / 4).backward(); a.grad      → 0.25
a = Value(2.0); (8 / a).backward(); a.grad      → -2.0     d(8/a)/da = -8/a²
a = Value(-1.0); a.relu().backward(); a.grad    → 0.0
a ** Value(2.0)                                  → TypeError
```

## Constraints

- Expressions have at most a few hundred nodes; inputs keep every intermediate finite.
- Plain Python and `math` only.

## Hints

1. What is the local derivative of `a ** k` with respect to `a`? Why does allowing a `Value` exponent need a different derivative that you are not writing here?
2. The derivative of `e^x` is `e^x`, and ReLU's derivative is 0 or 1. Which forward result can each backward step reuse?
3. If `a - b` is literally `a + (b * -1)`, which backward steps run when you call `backward()`? Do you need to write any new calculus for subtraction or division?
4. When Python evaluates `2 * a`, it first tries `int.__mul__(2, a)`. What does that return, and which method of `a` does Python try next? For `2 - a`, is it enough to call `a - 2`?

## Explain-back

- Why is building `-`, `/` and unary `-` from `+`, `*` and `**` safer than hand-deriving their backward steps?
- `2 - a` and `a - 2` need different reflected handling from `2 + a` and `a + 2`. Why?
- What does the numeric-gradient harness actually compare, and why is it the standard way to test an autograd engine?
- Your engine does one multiplication per Python object. Where does the real slowness of scalar autograd come from, and what does PyTorch do instead?
