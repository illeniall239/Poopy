# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
def early_stopping_epoch(val_losses: list[float], patience: int) -> int:
    if not val_losses or patience < 1:
        raise ValueError("need at least one loss and patience >= 1")
    best_epoch = 0
    bad_epochs = 0
    for epoch in range(1, len(val_losses)):
        if val_losses[epoch] < val_losses[best_epoch]:
            best_epoch = epoch
            bad_epochs = 0
        else:
            bad_epochs += 1
            if bad_epochs == patience:
                break
    return best_epoch


def diagnose(train_losses: list[float], val_losses: list[float], target_loss: float, max_gap: float) -> str:
    if not train_losses or len(train_losses) != len(val_losses):
        raise ValueError("loss curves must be non-empty and the same length")
    train, val = train_losses[-1], val_losses[-1]
    if train > target_loss:
        return "underfit"
    if val - train > max_gap:
        return "overfit"
    return "ok"
