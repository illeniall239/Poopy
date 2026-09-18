# Plot learning curves

Topic: 6. Visualization with matplotlib
Difficulty: 2 of 3

## Problem

Write `plot_learning_curves(train_loss: list[float], val_loss: list[float], title: str = "Learning curves") -> matplotlib.figure.Figure` with matplotlib (required) using the `Figure`/`Axes` API and never showing a window:

- One `Figure` with one `Axes`, created with `plt.subplots()` or `Figure()` directly.
- Two lines: epochs `1..n` on the x axis against `train_loss` (label `"train"`) and against `val_loss` (label `"validation"`), drawn in that order with `ax.plot`.
- x axis labelled `"epoch"`, y axis labelled `"loss"`, the title set, and a legend showing the two labels.
- If the best (lowest) validation loss occurs at epoch `k`, draw a vertical dashed line at `x = k` with `ax.axvline` so the plateau is visible.
- Raise `ValueError` if the two lists differ in length or are empty.

Return the `Figure`; do not call `plt.show()` and do not save anything. The test sets `matplotlib.use("Agg")` before importing your module and reads the data back from the `Axes`.

## Examples

```
fig = plot_learning_curves([1.0, 0.6, 0.4, 0.3], [1.1, 0.7, 0.65, 0.7])
ax = fig.axes[0]
ax.get_lines()[0].get_xdata()   → [1, 2, 3, 4]
ax.get_lines()[0].get_ydata()   → [1.0, 0.6, 0.4, 0.3]
ax.get_lines()[1].get_label()   → "validation"
ax.get_xlabel(), ax.get_ylabel() → "epoch", "loss"
ax.get_legend() is not None     → True
best epoch = 3, so a vertical line sits at x = 3
```

## Constraints

- Up to 10 000 epochs.
- The two loss lines are the first two `Line2D` objects on the Axes, in order; the `axvline` may come after.
- Only `matplotlib` (and the standard library) is needed.

## Hints

1. `fig, ax = plt.subplots()` returns two objects. Which one do you draw on, and which one do you return?
2. `ax.plot(y)` alone would start the x axis at 0. What list do you pass as x so the first epoch is 1?
3. The legend shows nothing unless the lines have labels. Where does the label go, and which call makes the legend appear?
4. Which built-in gives the position of the smallest value in `val_loss`, and how do you turn that 0-based position into an epoch number?

## Explain-back

- Training loss keeps falling while validation loss rises after epoch 6. What is the model doing, and what does the dashed line suggest you do?
- Why is a line chart right for loss over epochs but wrong for accuracy per country?
- A colleague's loss plot starts its y axis at 0.29 and the curve looks like a cliff. What is misleading, and what does `ax.set_ylim(0, ...)` change?
- Loss values span from 100 to 0.01 over training. Which axis scale shows the last epochs, and how do you set it on an `Axes`?
