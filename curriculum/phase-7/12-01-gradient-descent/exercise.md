# Gradient descent

Topic: 12. Optimization basics
Difficulty: 1 of 3

## Problem

Write `gradient_descent(grad_f: Callable[[list[float]], list[float]], x0: list[float], lr: float, steps: int) -> list[list[float]]` in pure Python (no NumPy).

Starting from `x0`, repeat `steps` times: `x = x - lr * grad_f(x)` (elementwise). Return the trajectory: a list of `steps + 1` points starting with a copy of `x0` and ending with the final `x`. Each point is a new list; never mutate `x0` or a point already in the trajectory. Raise `ValueError` if `lr <= 0` or `steps < 0`.

## Examples

```
grad = lambda x: [2 * x[0]]                    f(x) = x², curvature L = 2
gradient_descent(grad, [1.0], lr=0.1, steps=3)
→ [[1.0], [0.8], [0.64], [0.512]]              each step multiplies by (1 - lr·L) = 0.8

gradient_descent(grad, [1.0], lr=0.5, steps=1)  → [[1.0], [0.0]]     lr = 1/L jumps to the minimum
gradient_descent(grad, [1.0], lr=1.0, steps=3)  → [[1.0], [-1.0], [1.0], [-1.0]]   lr = 2/L oscillates
gradient_descent(grad, [1.0], lr=1.1, steps=3)  → |x| grows every step: lr > 2/L diverges

grad2 = lambda x: [2 * x[0], 20 * x[1]]        f = x² + 10y²
gradient_descent(grad2, [1.0, 1.0], lr=0.05, steps=100)[-1]  → close to [0, 0]
```

## Constraints

- Up to 10 000 steps and 100 dimensions.
- `grad_f` is called exactly `steps` times.
- The test checks convergence on quadratics against the closed form `x_k = (1 - lr·L)^k · x_0` within `1e-9`.

## Hints

1. Write one update for one coordinate. Which built-in pairs each coordinate of `x` with the matching coordinate of the gradient?
2. `x = x - lr * g` on lists: what does `-` do to two Python lists? What do you need instead?
3. If you append the same list object and then mutate it, what does the trajectory look like at the end?
4. For `f(x) = x²`, write `x_{k+1}` in terms of `x_k` and `lr`. For which `lr` does `|x|` shrink, stay, or grow?

## Explain-back

- A loss that grows every step: bug or learning rate? How would you tell in two lines of code?
- For a quadratic with curvature `L`, why does `lr > 2/L` diverge and `lr = 1/L` converge in one step? What does that suggest for a loss with different curvature along different axes?
- Why is stopping after a fixed number of steps a weak criterion? Name two others.
- Gradient descent found the minimum of `x² + 10y²`. Would it find the global minimum of a neural network loss? What does convexity buy you?
