# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
def sgd_momentum_step(params: list[float], grads: list[float], state: list[float], lr: float, beta: float) -> list[float]:
    if len(grads) != len(params):
        raise ValueError("params and grads must have the same length")
    if state and len(state) != len(params):
        raise ValueError("state must be empty or match params")
    if lr <= 0 or not 0 <= beta < 1:
        raise ValueError("need lr > 0 and 0 <= beta < 1")

    if not state:
        state.extend([0.0] * len(params))
    for i, g in enumerate(grads):
        state[i] = beta * state[i] + g
        params[i] -= lr * state[i]
    return state
