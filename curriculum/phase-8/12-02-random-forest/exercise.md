# Random forest

Topic: 12. Ensembles: bagging, random forests and gradient boosting
Difficulty: 3 of 3

## Problem

A random forest is bagging of deep trees plus one more source of randomness: every split looks at only a random subset of the features. Write a pure-Python class:

```
RandomForest(n_trees: int = 25, max_features: int | None = None, max_depth: int | None = None,
             min_samples: int = 2, seed: int = 0)
```

- `fit(X: list[list[float]], y: list) -> RandomForest` creates `rng = random.Random(seed)`, then grows `n_trees` classification trees and stores them, in order, in the attribute `self.trees` (a list). It returns `self`.
- `predict(X: list[list[float]]) -> list` returns, for each row, the majority vote of the trees, a tie going to the smallest label. Raise `RuntimeError` if `fit` has not been called.

Each tree is grown like the tree of exercise `11-03`, with two changes:

1. **Bootstrap.** The tree is trained on `n` rows drawn with replacement: `rows = [rng.randrange(n) for _ in range(n)]`.
2. **Feature subsets.** At every node that reaches the split step, draw `features = rng.sample(range(d), max_features)` and search the best split among those features only. `max_features=None` means `max(1, int(math.sqrt(d)))`.

Everything else is exactly `11-03`: Gini gain with children weighted by size, midpoint thresholds, ties to the smaller feature then the smaller threshold, no split unless its gain is above `1e-12`, a leaf when the depth reaches `max_depth` (`None` = unlimited) or the node has fewer than `min_samples` rows, leaf value = majority label with ties to the smallest. Trees use the same nested-dict format: `{"value": label}` leaves and `{"feature", "threshold", "left", "right"}` nodes, `<= threshold` going left. The tests read `tree["feature"]` at each root.

`fit` raises `ValueError` if `X` is empty, `len(X) != len(y)`, `n_trees < 1`, or `max_features` is not between 1 and `d`.

Your file must be standalone: it contains its own Gini, best-split and tree-growing code. You may copy them from your `11-02` and `11-03` solutions, changing the split search to take the list of allowed features, and your `bootstrap_sample` idea from `12-01`.

## Examples

```
X = [[float(i), float(i % 3)] for i in range(30)]
y = ["small"] * 15 + ["big"] * 15
forest = RandomForest(n_trees=9, max_features=1, seed=2).fit(X, y)
len(forest.trees)                          → 9
forest.predict([[0.0, 0.0], [29.0, 2.0]])  → ["small", "big"]
RandomForest(n_trees=3, max_features=5).fit(X, y)   → ValueError   only 2 features
```

On a noisy toy set (label `x0 + x1 > 0` with 20% of labels flipped, two useless extra features) the forest's held-out accuracy is several points above a single full-depth tree's.

## Constraints

- Pure Python: `random`, `math` and `collections` are allowed, numpy is not.
- Tests use at most 150 training rows, 4 features and 25 trees; the straightforward split search from `11-02` is fast enough.
- All randomness comes from the one `random.Random(seed)` made in `fit`, so the same seed gives the same trees.

## Hints

1. Where in your `11-03` code does the split search choose which features to try, and what is the smallest change that makes it try only some of them?
2. Why draw the feature subset at every node rather than once per tree? What would a tree look like if its one subset happened to miss the best feature?
3. If one feature is far stronger than the rest, which feature would every tree use at the root without subsets, and what does that do to how similar the trees' mistakes are?
4. Your forest has 25 trees that each fit their bootstrap sample perfectly. Where does its better held-out accuracy come from if every single tree overfits?

## Explain-back

- Why do random feature subsets make the forest better even though each tree gets worse? Connect it to how correlated the trees' errors are.
- Someone's forest overfits, so they cut it from 500 trees to 20. Does adding trees make a random forest overfit? What would you tune instead?
- A column with thousands of unique values ranks first in impurity-based importance. Why might that be misleading, and why is the importance not a causal effect?
- For a new tabular problem, which model family would you try before a neural network, and what baseline would a deep model have to beat?
