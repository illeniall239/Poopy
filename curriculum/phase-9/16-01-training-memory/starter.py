def param_memory_mb(n_params: int, dtype: str) -> float:
    """Return the MB (1024*1024 bytes) needed to store n_params numbers of the given dtype."""
    raise NotImplementedError


def adam_training_memory_mb(n_params: int) -> float:
    """Return the MB for float32 weights, gradients and Adam's two moment buffers."""
    raise NotImplementedError
