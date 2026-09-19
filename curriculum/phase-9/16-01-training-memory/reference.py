# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
BYTES = {"float64": 8, "float32": 4, "float16": 2, "bfloat16": 2}
MB = 1024 * 1024


def param_memory_mb(n_params: int, dtype: str) -> float:
    if dtype not in BYTES:
        raise ValueError(f"unknown dtype {dtype!r}")
    if n_params < 0:
        raise ValueError("n_params must be non-negative")
    return n_params * BYTES[dtype] / MB


def adam_training_memory_mb(n_params: int) -> float:
    # weights + gradients + Adam's first and second moments: four float32 copies
    return 4 * param_memory_mb(n_params, "float32")
