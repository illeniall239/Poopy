# Exact Shapley values

Topic: 13. Interpretability for tabular models
Difficulty: 3 of 3

## Problem

Shapley values split one prediction fairly among the features. Here the question is: the model says `f(x)` for this row and `f(background)` for a reference row; how much of the difference `f(x) − f(background)` does each feature account for? Write it exactly, by enumeration, with NumPy:

```
shapley_values(predict, x: np.ndarray, background: np.ndarray) -> np.ndarray
```

- `predict` maps an `(m, d)` array to `m` predictions (an already-trained model; nothing is retrained).
- For a coalition `S` (a set of feature indices), build the row `z` with `z[j] = x[j]` for `j` in `S` and `z[j] = background[j]` otherwise, and let `v(S) = predict(z[None, :])[0]`. So `v(∅) = f(background)` and `v(all) = f(x)`.
- Feature `i`'s Shapley value is

```
φᵢ = Σ over S ⊆ N \ {i}  of  |S|! · (d − |S| − 1)! / d!  ·  ( v(S ∪ {i}) − v(S) )
```

  where `N = {0, …, d−1}` and `|S|` is the coalition's size. The weight is the share of feature orderings in which exactly the features of `S` come before `i`.
- Return a float array of shape `(d,)`.

The values always add up to `f(x) − f(background)` (the efficiency property). A feature the model ignores gets exactly 0, and two features that play identical roles get equal values.

Raise `ValueError` if `x` is not 1-D, `x` and `background` have different shapes, or `d` is not between 1 and 4.

## Examples

```
f = lambda A: 3 * A[:, 0] + 2 * A[:, 1]
shapley_values(f, np.array([1.0, 1.0]), np.array([0.0, 0.0]))   → [3.0, 2.0]
f = lambda A: A[:, 0] * A[:, 1]
shapley_values(f, np.array([2.0, 3.0]), np.array([0.0, 0.0]))   → [3.0, 3.0]    the interaction is split evenly
f = lambda A: A[:, 0] ** 2
shapley_values(f, np.array([3.0, 7.0]), np.array([1.0, 0.0]))   → [8.0, 0.0]
```

## Constraints

- NumPy allowed; `itertools` and `math` too; no scikit-learn, no `shap`.
- `d` ≤ 4, so at most `4 · 2³ = 32` coalition pairs; evaluating `predict` once per coalition value is fine.
- Results within `1e-9` of the exact values.

## Hints

1. For `d = 2`, write out every coalition that does not contain feature 0. How many are there, and what weight does each get?
2. What row do you feed the model to evaluate a coalition, and why does that let you "remove" a feature from a model that always needs all `d` inputs?
3. The weights over all coalitions of one size must share something. For a fixed `i`, what do all the weights add up to, and why does that make the values average marginal contributions?
4. Before trusting your code, what should `sum(φ)` equal, and what should `φ` be for a linear model `w·x`?

## Explain-back

- Why does computing Shapley values not require retraining the model without each feature? What stands in for "the feature is missing"?
- For `f = x0 · x1` both features get half of the interaction. Why is that the fair split, and what would an order-dependent attribution have given instead?
- Exact enumeration costs `2^d` model calls per feature. Why is that fine here but not for 200 features, and what does SHAP do about it?
- A customer's loan was declined and "income" has the largest negative Shapley value. What can you tell the customer, and what can you not claim about what would happen if their income changed?
