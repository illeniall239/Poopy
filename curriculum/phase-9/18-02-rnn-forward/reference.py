# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
import math


def _matvec(M: list[list[float]], v: list[float]) -> list[float]:
    return [sum(m * x for m, x in zip(row, v)) for row in M]


def rnn_forward(
    xs: list[list[float]],
    h0: list[float],
    Wxh: list[list[float]],
    Whh: list[list[float]],
    b: list[float],
) -> list[list[float]]:
    H = len(h0)
    if len(Wxh) != H or len(b) != H or len(Whh) != H or any(len(row) != H for row in Whh):
        raise ValueError("h0, b, Whh and Wxh disagree on the hidden size")
    D = len(Wxh[0]) if Wxh else 0
    if any(len(row) != D for row in Wxh):
        raise ValueError("Wxh rows must all have the same length")

    h, states = h0, []
    for x in xs:
        if len(x) != D:
            raise ValueError("input vector has the wrong length")
        h = [math.tanh(a + r + bi) for a, r, bi in zip(_matvec(Wxh, x), _matvec(Whh, h), b)]
        states.append(h)
    return states
