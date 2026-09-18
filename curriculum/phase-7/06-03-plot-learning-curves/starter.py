import matplotlib.pyplot as plt
from matplotlib.figure import Figure


def plot_learning_curves(train_loss: list[float], val_loss: list[float], title: str = "Learning curves") -> Figure:
    """Figure with train and validation loss vs epoch, labelled axes, legend and a dashed line at the best epoch."""
    raise NotImplementedError
