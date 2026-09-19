# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
def label_smoothed_targets(k: int, target: int, eps: float) -> list[float]:
    if k < 2:
        raise ValueError("need at least two classes")
    if not 0 <= target < k:
        raise ValueError("target out of range")
    if not 0 <= eps < 1:
        raise ValueError("eps must be in [0, 1)")
    probs = [eps / k] * k        # the mass spread uniformly over all classes
    probs[target] += 1.0 - eps   # the rest stays on the true class
    return probs
