# Grid search space

Topic: 20. The practical workflow: a scikit-learn-style capstone
Difficulty: 1 of 3

## Problem

Grid search tries every combination of hyperparameter values. Write one pure-Python function:

`grid(space: dict[str, list]) -> list[dict]`

`space` maps each hyperparameter name to the list (or tuple) of values to try. Return the Cartesian product as a list of dicts, one per configuration, each holding one value for every name. The order is fixed so that runs are reproducible: sort the names alphabetically; the configurations then come out like nested loops over the sorted names, with the **last** name changing fastest and each name's values in the order given. This is the order of scikit-learn's `ParameterGrid`.

An empty `space` has exactly one configuration, `{}`. Raise `ValueError` if any value is not a list or tuple, or is empty. Every returned dict is a separate object.

## Examples

```
grid({"lr": [0.1, 0.01], "depth": [2, 4, 8]})
    → [{"depth": 2, "lr": 0.1}, {"depth": 2, "lr": 0.01},
       {"depth": 4, "lr": 0.1}, {"depth": 4, "lr": 0.01},
       {"depth": 8, "lr": 0.1}, {"depth": 8, "lr": 0.01}]
grid({})                → [{}]
grid({"lr": []})        → ValueError
grid({"lr": 0.1})       → ValueError
```

## Constraints

- Pure Python: `itertools` is allowed.
- The product can be large; build it in O(size of the output).

## Hints

1. With 3 depths and 2 learning rates, how many configurations are there? In general, how does the count grow with each new hyperparameter?
2. Which function in `itertools` already produces the Cartesian product of several lists, and in what order does it vary its inputs?
3. How do you turn one tuple from that product back into a dict with the right names?
4. What is the product of zero lists: no configurations, or one empty configuration?

## Explain-back

- You try learning rates `[0.1, 0.2, 0.3]`. Why is that a poor grid, and what spacing would you use instead?
- Five hyperparameters with ten values each: how many fits is that with 5-fold cross-validation, and what does that suggest about grids?
- Why does the order of configurations matter for reproducibility, even though each one is evaluated independently?
- After searching 2 000 configurations, the best validation score is 0.94. Why is that likely an optimistic estimate of the test score?
