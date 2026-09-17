# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
def subsets(nums: list[int]) -> list[list[int]]:
    result: list[list[int]] = []
    path: list[int] = []

    def explore(i: int) -> None:
        if i == len(nums):
            result.append(path.copy())
            return
        path.append(nums[i])
        explore(i + 1)
        path.pop()
        explore(i + 1)

    explore(0)
    return result
