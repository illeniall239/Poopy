# A Value with add, mul and tanh

Topic: 4. A scalar autograd engine (micrograd)
Difficulty: 2 of 3

## Problem

Start your own autograd engine. In plain Python (the `math` module is fine; no numpy, no torch), write a class `Value` that wraps one number and remembers how it was computed, so that `backward()` can fill in the gradient of every value that led to it.

- `Value(data, _children=(), _op="")`: store `data` (a number) in `self.data`; set `self.grad = 0.0`. `_children` are the `Value`s this one was computed from and `_op` is a label for the operation (useful for debugging, not tested). Each `Value` also needs a way to push its gradient back to its children, typically a `self._backward` function that does nothing for a leaf.
- `a + b` and `a * b` return a new `Value`. `b` may be a `Value` or a plain `int`/`float`; wrap plain numbers in a `Value` first, so `v + 2` and `v * 2` work. (`2 + v` and `2 * v` are **not** required yet.)
- `a.tanh()` returns a new `Value` holding `tanh(a.data)`.
- `out.backward()` computes `∂out/∂v` for every `Value` `v` that `out` was built from and stores it in `v.grad`: set `out.grad = 1.0`, order all values reachable from `out` topologically, and call each one's backward step in reverse order. Each backward step must **add** into its children's `grad` (`+=`), never assign, because a value can be used more than once: in `a + a` or `a * a`, both uses contribute.

You can assume `backward()` is called once per freshly built expression; tests never call it twice on the same graph.

## Examples

```
a = Value(2.0); b = Value(-3.0)
(a * b + 1).data               → -5.0

a = Value(3.0); c = a + a; c.backward()
a.grad                          → 2.0                both uses of a count

a = Value(3.0); c = a * a; c.backward()
a.grad                          → 6.0

x1, x2, w1, w2 = Value(2.0), Value(0.0), Value(-3.0), Value(1.0)
b = Value(6.881373587019543)
o = (x1 * w1 + x2 * w2 + b).tanh(); o.backward()
o.data                          → 0.7071067811865476
(x1.grad, w1.grad, x2.grad, w2.grad) → (-1.5, 1.0, 0.5, 0.0)
```

## Constraints

- Expressions have at most a few hundred nodes.
- Gradients are checked against hand-computed values and central-difference numeric gradients within `1e-6`.

## Hints

1. For `out = a + b` and `out = a * b`, what is the local derivative of `out` with respect to `a` and to `b`? What does each child receive, given `out.grad`?
2. Where can the backward step for `out` live so that it still knows `a`, `b` and `out` when it is called later? (Think about closures.)
3. What goes wrong in `a + a` if the backward step writes `a.grad = out.grad` instead of adding to it?
4. Why is recursing from `out` into its children and calling their backward steps immediately not enough when a value feeds two places at different depths? What order guarantees a value's `grad` is complete before it is passed on?

## Explain-back

- Walk through `a + a` with `grad =` instead of `grad +=`. Which number do you get, and why is it wrong?
- `backward()` starts by setting `out.grad = 1.0`. What is that number, and what would every gradient be if you forgot it?
- The derivative of `tanh` can be computed from the output alone: `1 − t²`. Why is that convenient in the backward step?
- Why does `backward()` need a topological order rather than plain recursion from the output?
