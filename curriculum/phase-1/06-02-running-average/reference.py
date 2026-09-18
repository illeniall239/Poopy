# Reference solution: only used by scripts/verify-exercises.mjs. Shown in the Breakdown only after the Learner's own solution passes.
def running_averages(nums: list[float]) -> list[float]:
    result = []
    total = 0
    for i in range(len(nums)):
        total += nums[i]
        result.append(total / (i + 1))
    return result
