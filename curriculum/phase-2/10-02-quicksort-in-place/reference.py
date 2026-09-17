# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
import random


def quick_sort(nums: list[int]) -> None:
    _sort_range(nums, 0, len(nums) - 1)


def _sort_range(nums: list[int], lo: int, hi: int) -> None:
    while lo < hi:
        pivot = nums[random.randint(lo, hi)]
        # Three regions: [lo, lt) < pivot, [lt, i) == pivot, (gt, hi] > pivot.
        lt, i, gt = lo, lo, hi
        while i <= gt:
            if nums[i] < pivot:
                nums[i], nums[lt] = nums[lt], nums[i]
                i += 1
                lt += 1
            elif nums[i] > pivot:
                nums[i], nums[gt] = nums[gt], nums[i]
                gt -= 1
            else:
                i += 1
        # Recurse into the smaller side and loop on the larger one to keep the stack O(log n).
        if lt - lo < hi - gt:
            _sort_range(nums, lo, lt - 1)
            lo = gt + 1
        else:
            _sort_range(nums, gt + 1, hi)
            hi = lt - 1
