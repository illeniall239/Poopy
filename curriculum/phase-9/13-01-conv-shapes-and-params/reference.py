# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
def conv_output_size(n: int, k: int, p: int, s: int) -> int:
    if n < 1 or k < 1 or p < 0 or s < 1:
        raise ValueError("need n, k, s >= 1 and p >= 0")
    if k > n + 2 * p:
        raise ValueError("kernel is larger than the padded input")
    return (n + 2 * p - k) // s + 1


def conv_params(in_c: int, out_c: int, k: int, bias: bool = True) -> int:
    if in_c < 1 or out_c < 1 or k < 1:
        raise ValueError("channels and kernel size must be at least 1")
    return out_c * in_c * k * k + (out_c if bias else 0)
