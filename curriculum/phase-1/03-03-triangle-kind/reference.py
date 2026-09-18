# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
def triangle_kind(a: int, b: int, c: int) -> str:
    positive = a > 0 and b > 0 and c > 0
    closes = a + b > c and a + c > b and b + c > a
    if not positive or not closes:
        return "invalid"
    if a == b and b == c:
        return "equilateral"
    if a == b or b == c or a == c:
        return "isosceles"
    return "scalene"
