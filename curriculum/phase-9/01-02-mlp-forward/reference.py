# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
from typing import Callable

Layer = tuple[list[list[float]], list[float], Callable[[float], float]]


def mlp_forward(x: list[float], layers: list[Layer]) -> list[float]:
    for W, b, act in layers:
        out = []
        for row, bias in zip(W, b):
            if len(row) != len(x):
                raise ValueError("layer width does not match its input")
            out.append(act(sum(wi * xi for wi, xi in zip(row, x)) + bias))
        x = out
    return list(x)
