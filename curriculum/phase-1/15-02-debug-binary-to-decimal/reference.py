# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
def binary_to_decimal(bits: str) -> int:
    if len(bits) == 0:
        raise ValueError("Binary string is empty")
    for ch in bits:
        if ch != "0" and ch != "1":
            raise ValueError(f'Not a binary string: "{bits}"')

    result = 0
    place_value = 1
    for i in range(len(bits) - 1, -1, -1):
        if bits[i] == "1":
            result += place_value
        place_value *= 2
    return result
