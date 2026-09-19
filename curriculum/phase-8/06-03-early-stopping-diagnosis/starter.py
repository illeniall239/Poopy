def early_stopping_epoch(val_losses: list[float], patience: int) -> int:
    """Return the index of the epoch whose weights early stopping with this patience keeps."""
    raise NotImplementedError


def diagnose(train_losses: list[float], val_losses: list[float], target_loss: float, max_gap: float) -> str:
    """Return "underfit", "overfit" or "ok" from the final losses and their gap."""
    raise NotImplementedError
