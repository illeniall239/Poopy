def conv2d(image: list[list[float]], kernel: list[list[float]], stride: int = 1, padding: int = 0) -> list[list[float]]:
    """Single-channel 2-D cross-correlation (no kernel flip) with zero padding and stride."""
    raise NotImplementedError


def maxpool2d(image: list[list[float]], size: int, stride: int | None = None) -> list[list[float]]:
    """Max over each size x size window; stride defaults to size."""
    raise NotImplementedError
