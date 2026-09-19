# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import math


def adam_step(params: list[float], grads: list[float], state: dict[str, list[float]],
              lr: float, b1: float, b2: float, eps: float, t: int) -> list[float]:
    n = len(params)
    if len(grads) != n:
        raise ValueError("params and grads must have the same length")
    if t < 1 or lr <= 0 or eps <= 0 or not (0 <= b1 < 1 and 0 <= b2 < 1):
        raise ValueError("need t >= 1, lr > 0, eps > 0 and betas in [0, 1)")
    if state and (len(state.get("m", ())) != n or len(state.get("v", ())) != n):
        raise ValueError("state m and v must match params")

    if not state:
        state["m"] = [0.0] * n
        state["v"] = [0.0] * n
    m, v = state["m"], state["v"]
    correction1 = 1 - b1 ** t
    correction2 = 1 - b2 ** t
    for i, g in enumerate(grads):
        m[i] = b1 * m[i] + (1 - b1) * g
        v[i] = b2 * v[i] + (1 - b2) * g * g
        m_hat = m[i] / correction1
        v_hat = v[i] / correction2
        params[i] -= lr * m_hat / (math.sqrt(v_hat) + eps)
    return params
