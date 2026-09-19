# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
Net = tuple[list[list[float]], list[float], list[list[float]], list[float]]


def xor_net() -> Net:
    # hidden 0 = relu(x1 + x2)      (OR-like: 0,1,1,2)
    # hidden 1 = relu(x1 + x2 - 1)  (AND-like: 0,0,0,1)
    # out = h0 - 2*h1               (0,1,1,0)
    return ([[1.0, 1.0], [1.0, 1.0]], [0.0, -1.0], [[1.0, -2.0]], [0.0])


def predict(x: list[float], net: Net) -> int:
    W1, b1, W2, b2 = net
    h = [max(0.0, sum(w * xi for w, xi in zip(row, x)) + b) for row, b in zip(W1, b1)]
    out = sum(w * hi for w, hi in zip(W2[0], h)) + b2[0]
    return 1 if out > 0.5 else 0
