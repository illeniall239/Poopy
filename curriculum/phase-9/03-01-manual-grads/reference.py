# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
def manual_grads(a: float, b: float, c: float, f: float) -> dict[str, float]:
    # forward: keep the intermediate values, the backward pass needs them
    e = a * b
    d = e + c

    # backward: upstream gradient times local derivative, node by node
    dL = 1.0
    dd = dL * f      # L = d * f
    df = dL * d
    de = dd * 1.0    # d = e + c: addition passes the gradient through
    dc = dd * 1.0
    da = de * b      # e = a * b
    db = de * a
    return {"a": da, "b": db, "c": dc, "f": df}
