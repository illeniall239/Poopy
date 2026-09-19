import torch


def lstm_cell(
    x: torch.Tensor, h: torch.Tensor, c: torch.Tensor, params: dict[str, torch.Tensor]
) -> tuple[torch.Tensor, torch.Tensor]:
    """One LSTM step with gates in order i, f, g, o; return (h_new, c_new)."""
    raise NotImplementedError
