# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
from torch import nn


def _check(model: nn.Module) -> None:
    if not isinstance(model, nn.Sequential) or len(model) == 0 or not isinstance(model[-1], nn.Linear):
        raise ValueError("model must be an nn.Sequential ending in an nn.Linear head")


def freeze_backbone(model: nn.Sequential) -> nn.Sequential:
    _check(model)
    for p in model[:-1].parameters():
        p.requires_grad = False
    for p in model[-1].parameters():
        p.requires_grad = True
    return model


def replace_head(model: nn.Sequential, n_classes: int) -> nn.Sequential:
    _check(model)
    if n_classes < 1:
        raise ValueError("n_classes must be at least 1")
    model[-1] = nn.Linear(model[-1].in_features, n_classes)
    return model
