# Fraction of dead ReLUs

Topic: 2. Activation functions
Difficulty: 2 of 3

## Problem

A ReLU unit is **dead** on a dataset when it never fires: its pre-activation is `≤ 0` for every example, so its output is always 0 and its incoming weights always receive zero gradient.

Write `fraction_dead(pre_acts)`. `pre_acts` is the matrix of pre-activations of one ReLU layer for a batch: one row per example, one column per unit (so `pre_acts[i][j]` is unit `j` on example `i`). It may be a list of lists of floats or a 2-D NumPy array; NumPy is allowed but not required. Return, as a Python `float`, the fraction of **units (columns)** that are dead. A pre-activation of exactly `0` counts as not firing.

Raise `ValueError` if there are no rows, no columns, or the rows have different lengths.

## Examples

```
fraction_dead([[ 1.0, -2.0, 0.0],
               [-1.0, -0.5, 0.0]])            → 0.6666666666666666   units 1 and 2 never fire
fraction_dead([[-1.0, 3.0]])                  → 0.5
fraction_dead([[ 0.1, -1.0],
               [-5.0,  2.0]])                 → 0.0                  each unit fires at least once
fraction_dead([[ 1.0, 2.0], [3.0]])           → ValueError
```

## Constraints

- Up to 10 000 rows and 1 000 columns.
- Entries are finite floats.

## Hints

1. Is "dead" a property of one number, one example (row), or one unit (column)?
2. For a single unit, which question about its whole column decides whether it is dead: "is any entry positive?" or "is the average negative?"
3. A unit that is negative on 99% of examples and positive on 1%: is it dead? Does it still learn?
4. How do you walk a list of lists column by column (think `zip(*rows)`), or reduce over the right axis in NumPy?

## Explain-back

- Why does a dead ReLU unit stay dead under gradient descent? What gradient reaches its weights and bias?
- Name two things that can kill many ReLU units at once during training.
- Counting zero entries (fraction of outputs that are 0) gives a different number from counting dead units. Why is only the second one a sign of a problem?
- Does Leaky ReLU or GELU have dead units in this sense? Why?
