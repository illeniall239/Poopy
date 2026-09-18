# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
def broadcast_shape(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    n = max(len(a), len(b))
    a = (1,) * (n - len(a)) + tuple(a)
    b = (1,) * (n - len(b)) + tuple(b)
    out = []
    for p, q in zip(a, b):
        if p == q or q == 1:
            out.append(p)
        elif p == 1:
            out.append(q)
        else:
            raise ValueError(f"shapes {a} and {b} are not broadcastable")
    return tuple(out)
