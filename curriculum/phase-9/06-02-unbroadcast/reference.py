# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import numpy as np


def unbroadcast(grad: np.ndarray, shape: tuple[int, ...]) -> np.ndarray:
    grad = np.asarray(grad)
    shape = tuple(shape)
    extra = grad.ndim - len(shape)
    if extra < 0 or any(s not in (1, g) for s, g in zip(shape, grad.shape[extra:])):
        raise ValueError(f"shape {shape} does not broadcast to {grad.shape}")
    out = grad.sum(axis=tuple(range(extra)))  # axes that `shape` never had
    squeezed = tuple(i for i, (s, g) in enumerate(zip(shape, out.shape)) if s == 1 and g != 1)
    out = out.sum(axis=squeezed, keepdims=True)  # axes that were size 1
    return np.array(out).reshape(shape)
