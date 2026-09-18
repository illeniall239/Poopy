# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


def plot_learning_curves(train_loss: list[float], val_loss: list[float], title: str = "Learning curves") -> Figure:
    if not train_loss or len(train_loss) != len(val_loss):
        raise ValueError("train and validation losses must be non-empty and the same length")
    epochs = list(range(1, len(train_loss) + 1))
    fig, ax = plt.subplots()
    ax.plot(epochs, train_loss, label="train")
    ax.plot(epochs, val_loss, label="validation")
    best = min(range(len(val_loss)), key=val_loss.__getitem__) + 1
    ax.axvline(best, linestyle="--", color="gray")
    ax.set_xlabel("epoch")
    ax.set_ylabel("loss")
    ax.set_title(title)
    ax.legend()
    return fig
