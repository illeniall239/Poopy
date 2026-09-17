# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
def second_largest(nums: list[float]) -> float | None:
    largest = float("-inf")
    second = float("-inf")
    for n in nums:
        if n > largest:
            second = largest
            largest = n
        elif n < largest and n > second:
            second = n
    return None if second == float("-inf") else second
