from torch import nn


def freeze_backbone(model: nn.Sequential) -> nn.Sequential:
    """Make every parameter except the last (Linear head) module's untrainable; return the model."""
    raise NotImplementedError


def replace_head(model: nn.Sequential, n_classes: int) -> nn.Sequential:
    """Swap the last Linear for a new trainable Linear(in_features, n_classes); return the model."""
    raise NotImplementedError
