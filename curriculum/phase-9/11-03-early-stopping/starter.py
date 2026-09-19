def early_stopping_epoch(val_losses: list[float], patience: int) -> int | None:
    """Return the best epoch to restore once val loss fails to improve for `patience` epochs, else None."""
    raise NotImplementedError
