def mean_baseline(train_ys: list[float]) -> float:
    """Return the mean of the training targets; ValueError if empty."""
    raise NotImplementedError


def mse(y_true: list[float], y_pred: list[float]) -> float:
    """Return the mean squared error; ValueError on empty or mismatched lengths."""
    raise NotImplementedError


def baseline_mse(train_ys: list[float], val_ys: list[float]) -> float:
    """Return the MSE on val_ys of predicting the train mean everywhere."""
    raise NotImplementedError
