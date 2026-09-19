# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import numpy as np

ACTIVATIONS = {
    "linear": lambda z: z,
    "relu": lambda z: np.maximum(0.0, z),
    "tanh": np.tanh,
}


def simulate_depth_std(depth: int, width: int, init_std: float, act: str, seed: int) -> list[float]:
    if act not in ACTIVATIONS:
        raise ValueError(f"unknown activation {act!r}")
    if depth < 1 or width < 1 or init_std <= 0:
        raise ValueError("need depth >= 1, width >= 1 and init_std > 0")
    f = ACTIVATIONS[act]
    rng = np.random.default_rng(seed)
    x = rng.standard_normal((1000, width))
    stds = []
    for _ in range(depth):
        W = rng.standard_normal((width, width)) * init_std
        x = f(x @ W)
        stds.append(float(x.std()))
    return stds
