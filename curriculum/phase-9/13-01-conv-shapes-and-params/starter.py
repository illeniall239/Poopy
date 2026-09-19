def conv_output_size(n: int, k: int, p: int, s: int) -> int:
    """Return floor((n + 2p - k) / s) + 1, the output size of a conv along one dimension."""
    raise NotImplementedError


def conv_params(in_c: int, out_c: int, k: int, bias: bool = True) -> int:
    """Return the number of weights (plus biases) of a k x k Conv2d from in_c to out_c channels."""
    raise NotImplementedError
