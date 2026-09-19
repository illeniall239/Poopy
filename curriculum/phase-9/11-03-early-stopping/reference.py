# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
def early_stopping_epoch(val_losses: list[float], patience: int) -> int | None:
    if patience < 1:
        raise ValueError("patience must be at least 1")
    best, best_epoch, waited = float("inf"), None, 0
    for epoch, loss in enumerate(val_losses):
        if loss < best:
            best, best_epoch, waited = loss, epoch, 0
        else:
            waited += 1
            if waited >= patience:
                return best_epoch
    return None
