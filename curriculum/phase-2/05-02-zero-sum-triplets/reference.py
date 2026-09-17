# Reference solution: only used by scripts/verify-exercises.mjs. The Tutor never shows it (Socratic rule).
def zero_sum_triplets(values: list[int]) -> list[list[int]]:
    sorted_values = sorted(values)
    result: list[list[int]] = []
    for i in range(len(sorted_values) - 2):
        if i > 0 and sorted_values[i] == sorted_values[i - 1]:
            continue
        lo, hi = i + 1, len(sorted_values) - 1
        while lo < hi:
            total = sorted_values[i] + sorted_values[lo] + sorted_values[hi]
            if total < 0:
                lo += 1
            elif total > 0:
                hi -= 1
            else:
                result.append([sorted_values[i], sorted_values[lo], sorted_values[hi]])
                lo += 1
                while lo < hi and sorted_values[lo] == sorted_values[lo - 1]:
                    lo += 1
                hi -= 1
    return result
