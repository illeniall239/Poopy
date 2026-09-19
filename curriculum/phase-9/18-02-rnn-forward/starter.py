def rnn_forward(
    xs: list[list[float]],
    h0: list[float],
    Wxh: list[list[float]],
    Whh: list[list[float]],
    b: list[float],
) -> list[list[float]]:
    """Return [h_1, ..., h_T] with h_t = tanh(Wxh x_t + Whh h_{t-1} + b)."""
    raise NotImplementedError
