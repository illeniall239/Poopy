# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
def max_and_min(nums: list[float]) -> dict[str, float] | None:
    if len(nums) == 0:
        return None
    largest = nums[0]
    smallest = nums[0]
    for n in nums:
        if n > largest:
            largest = n
        if n < smallest:
            smallest = n
    return {"max": largest, "min": smallest}
